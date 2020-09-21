import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

center_dict = {'position':'absolute','top':'45vh','left':'30vw','width':'40vw',}

# please leave
leave_widget = html.Div(html.Div([
    html.H1('LEAVE this private page!', style={'font-size':'5vw', 'color':'#f00'}),
    html.P('or contact even311379@hotmail.com for permission')], style=center_dict
    ),
    id = 'leave_widget',
    style={'display':'none'}
)

# login app
login_widget = html.Div(
    html.Div([
        html.H3('Type the correct password:'),
        dcc.Input(
            id='password',
            type='password',
            debounce = True,
            placeholder = "Please Enter the valid password",
            value = ''),        
        ], style=center_dict
    ),
    id = 'login_widget',
    style={'display':'none'}
)

