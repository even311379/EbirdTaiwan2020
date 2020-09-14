import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from django.core.mail import EmailMessage
from django.template.loader import get_template

from fall.models import SignupData
from automation import passwords

app = DjangoDash(
    'Signup', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash


app.layout = html.Div([html.Div([    
    dbc.Container([
        html.Div([
            html.P('eBird公開顯示名稱', className="font-weight-bold", style={'margin-bottom':'1vh'}),
            dcc.Input(id='public_ebird_name', style={'margin-bottom':'3vh','width':'100%'}),
            html.P('選擇隊伍', className="font-weight-bold", style={'margin-bottom':'1vh'}),
            dcc.Dropdown(
                options=[
                    {'label': '彩鷸隊', 'value': '彩鷸隊'},
                    {'label': '家燕隊', 'value': '家燕隊'},
                    {'label': '大冠鷲隊', 'value': '大冠鷲隊'}
                ],
                clearable=False,
                placeholder="選擇你想加入的小隊",
                id='team_select',
                style={'margin-bottom':'3vh'}
            ),
            html.P('連絡信箱', className="font-weight-bold", style={'margin-bottom':'1vh'}),
            dcc.Input(type='email', id='email', style={'margin-bottom':'6vh','width':'100%'}),
            html.Div('提交並開始比賽!',id='submit_btn',className='fall_btn dash_btn01',style={'margin-bottom':'3vh'}),
            dbc.Row([
                dbc.Col(html.A('忘記公開顯示帳號',className='fall_btn dash_btn02'), width=5),
                dbc.Col('', width=2),
                dbc.Col(html.A('創建新帳號',className='fall_btn dash_btn02',href='https://secure.birds.cornell.edu/cassso/account/create?'), width=5),
            ], style={'margin-bottom':'1vh'}),
            html.P('', className="font-weight-bold text-danger", id='error_message'),    
        ], className='signup_container')]),
        html.A(html.I(className='fas fa-times fa-3x'),className='close_to_home',href='/'),
        html.Div(id='no_menu',style={'display':'none'}) # add this to hide menu bar (via brython)
    ], className='green_background') ,
    html.Div(id='thankyou_screen', className='thankyou_screen')
])



def send_validation_email(email, ebirdID, team):
    t = get_template('fall/welcome_email.html')
    content = t.render(locals())
    msg = EmailMessage(
        '認證ebirdTaiwn 秋季挑戰賽帳號',
        content,
        passwords.mailserver_account,
        [email]
    )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print(e)


@app.callback(
    [Output('thankyou_screen','style'),
    Output('error_message','children')],
    [Input('submit_btn', 'n_clicks')],
    [State('public_ebird_name','value'),
    State('team_select', 'value'),
    State('email','value'),]
)
def submit_signup(n_click, public_ebird_name, selected_team, email):    
    print('hey')
    print(public_ebird_name)
    print(selected_team)
    print(email)
    if (public_ebird_name == None or selected_team == None or email == None):
        return {'top':'100vh'}, '請填寫所有欄位'
    if ('@' not in email):
        print(123)
        return {'top':'100vh'}, '請輸入正確的email'
    if (len(SignupData.objects.filter(ebirdid=public_ebird_name)) > 0):
        print(456)
        return {'top':'100vh'}, '這筆eBird公開顯示名稱已經註冊了！'
    if (len(SignupData.objects.filter(email=email)) > 0):
        print(789)
        return {'top':'100vh'}, '這個email註冊過了！'
        
    NewSignupData = SignupData(
        ebirdid = public_ebird_name,
        team = selected_team,        
        email = email
    )
    NewSignupData.save()
    send_validation_email(email, public_ebird_name, selected_team)
    return {'top':'0vh'},''


