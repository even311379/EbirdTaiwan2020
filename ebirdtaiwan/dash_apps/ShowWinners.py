import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_table

import datetime, re
import pandas as pd

from fall.models import PredictionData, Survey, SurveyObs

app = DjangoDash(
    'ShowWinners', 
    add_bootstrap_links=True, 
) 

page0 = html.Div([
    html.Div('台北觀鳥大賽'),
    html.Div('得獎名單'),    
], className='winner_title', id='page0', style={'display':'block'})

page1 = html.Div([
    html.Div('三隊總成績', className='winner_stitle'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/farmbird.png", top=True, className='winner_card_img'),
                html.H2('彩鷸隊',className='card-title my-3'),
                html.Table([
                    html.Tr([html.Td('鳥種數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'},id='t1sn')]),
                    html.Tr([html.Td('鳥隻數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t1sc')]),
                    html.Tr([html.Td('清單數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t1nl')]),
                ], className='winner_table'),
                html.P(''),
                html.P(''),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/citybird.png", top=True, className='winner_card_img'),
                html.H2('家燕隊',className='card-title my-3'),
                html.Table([
                    html.Tr([html.Td('鳥種數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'},id='t2sn')]),
                    html.Tr([html.Td('鳥隻數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t2sc')]),
                    html.Tr([html.Td('清單數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t2nl')]),
                ], className='winner_table'),
                html.P(''),
                html.P(''),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/forestbird.png", top=True, className='winner_card_img'),
                html.H2('大冠鷲隊',className='card-title my-3'),
                html.Table([
                    html.Tr([html.Td('鳥種數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t3sn')]),
                    html.Tr([html.Td('鳥隻數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t3sc')]),
                    html.Tr([html.Td('清單數',style={'text-align':'left'}),html.Td('',style={'text-align':'right'}, id='t3nl')]),
                ], className='winner_table'),
                html.P(''),
                html.P(''),
            ]),width=4),           
    ], className='fff'),    
], id='page1', style={'display':'none'})

page2 = html.Div([
    html.Div('個人獎', className='winner_stitle'),
    html.Table([
        html.Tr([html.Td('鳥種數',style={'text-align':'left'}) ,html.Td('', id='pw1'), html.Td('',id='pw1d',style={'text-align':'right'})]),
        html.Tr([html.Td('鳥隻數',style={'text-align':'left'}) ,html.Td('', id='pw2'), html.Td('',id='pw2d',style={'text-align':'right'})]),
        html.Tr([html.Td('清單數',style={'text-align':'left'}) ,html.Td('', id='pw3'), html.Td('',id='pw3d',style={'text-align':'right'})]),
    ], className='winner_table2'),    
], id='page2', style={'display':'none'})

page3 = html.Div([
    html.Div('團體獎', className='winner_stitle'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="", top=True, className='winner_card_img',id='sn_img'),
                dbc.CardBody([
                    html.H1("鳥種數"),
                    html.Br(),
                    html.H1("",id='snwt'),
                    html.H1("",id='snwtd'),
                ]),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="", top=True, className='winner_card_img',id='sc_img'),
                dbc.CardBody([
                    html.H1("鳥隻數"),
                    html.Br(),
                    html.H1("",id='scwt'),
                    html.H1("",id='scwtd'),
                ]),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="", top=True, className='winner_card_img',id='nl_img'),
                dbc.CardBody([
                    html.H1("清單數"),
                    html.Br(),
                    html.H1("",id='nlwt'),
                    html.H1("",id='nlwtd'),
                ]),
            ]),width=4),           
    ], className='fff'),
],id='page3', style={'display':'none'})

page4 = html.Div([
    html.Div('猜猜樂得獎名單', className='winner_stitle'),
    dbc.Row("", className='fff', id='guess_result'),
],id='page4', style={'display':'none'})

page_index = 0

pages = [page0, page1, page2, page3, page4]

app.layout = html.Button([
    html.Div(pages,id='page_content'),
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'}),
    html.Div('',id='empty2',style={'display':'none'})
    ], id='Bg_btn', n_clicks=0)


app.clientside_callback(
    """
    function(path) {
        return String(window.innerWidth) + ',' + String(window.innerHeight);
    }    
    """,
    Output('empty', 'children'),
    [Input('url', 'pathname')]
)

@app.callback(
    [Output('t1sn','children'),
    Output('t1sc','children'),
    Output('t1nl','children'),
    Output('t2sn','children'),
    Output('t2sc','children'),
    Output('t2nl','children'),
    Output('t3sn','children'),
    Output('t3sc','children'),
    Output('t3nl','children'),
    Output('pw1','children'),
    Output('pw2','children'),
    Output('pw3','children'),
    Output('pw1d','children'),
    Output('pw2d','children'),
    Output('pw3d','children'),
    Output('sn_img','src'),
    Output('snwt','children'),
    Output('snwtd','children'),
    Output('sc_img','src'),
    Output('scwt','children'),
    Output('scwtd','children'),
    Output('nl_img','src'),
    Output('nlwt','children'),
    Output('nlwtd','children'),
    Output('guess_result','children'),],   
    [Input('empty', 'children')], 
    prevent_initial_call = True
)
def init_pages(h):
    global page_index
    page_index = 0
    # 三隊總成績    
    t1_rsn = SurveyObs.objects.filter(survey__team = '彩鷸隊', survey__is_valid=True).values_list('species_name', flat=True)
    t1sn = len(set([re.sub(r' ?\(.*?\)','',s) for s in t1_rsn]))
    t1sc = sum(SurveyObs.objects.filter(survey__team = '彩鷸隊', survey__is_valid=True).values_list('amount', flat=True))
    t1nl = len(Survey.objects.filter(team='彩鷸隊', is_valid=True))
    t2_rsn = SurveyObs.objects.filter(survey__team = '家燕隊', survey__is_valid=True).values_list('species_name', flat=True)
    t2sn = len(set([re.sub(r' ?\(.*?\)','',s) for s in t2_rsn]))
    t2sc = sum(SurveyObs.objects.filter(survey__team = '家燕隊', survey__is_valid=True).values_list('amount', flat=True))
    t2nl = len(Survey.objects.filter(team='家燕隊', is_valid=True))
    t3_rsn = SurveyObs.objects.filter(survey__team = '大冠鷲隊', survey__is_valid=True).values_list('species_name', flat=True)
    t3sn = len(set([re.sub(r' ?\(.*?\)','',s) for s in t3_rsn]))
    t3sc = sum(SurveyObs.objects.filter(survey__team = '大冠鷲隊', survey__is_valid=True).values_list('amount', flat=True))
    t3nl = len(Survey.objects.filter(team='大冠鷲隊', is_valid=True))
    # 個人獎
    all_participants = list(set(Survey.objects.filter(is_valid=True).values_list('creator', flat=True)))
    participants_sn = []
    participants_sc = []
    participants_nl = []
    
    for participant in all_participants:

        rsn = SurveyObs.objects.filter(survey__creator=participant, survey__is_valid=True).values_list('species_name', flat=True)
        participants_sn.append(len(set([re.sub(r' ?\(.*?\)','',s) for s in rsn])))
        participants_sc.append(sum(SurveyObs.objects.filter(survey__creator=participant, survey__is_valid=True).values_list('amount', flat=True)))
        participants_nl.append(len(Survey.objects.filter(creator=participant, is_valid=True)))
 
    pw1d = max(participants_sn)
    pw1 = all_participants[participants_sn.index(pw1d)]
    pw2d = max(participants_sc)
    pw2 = all_participants[participants_sc.index(pw2d)]
    pw3d = max(participants_nl)
    pw3 = all_participants[participants_nl.index(pw3d)]
    # 團體獎
    img_srcs = ["/static/img/fall/farmbird.png", "/static/img/fall/citybird.png", "/static/img/fall/forestbird.png"]
    team_names = ['彩鷸隊', '家燕隊', '大冠鷲隊']
    sns = [t1sn, t2sn, t3sn]
    sn_img = img_srcs[sns.index(max(sns))]
    snwt = team_names[sns.index(max(sns))]
    snwtd = max(sns)
    scs = [t1sc, t2sc, t3sc]
    sc_img = img_srcs[scs.index(max(scs))]
    scwt = team_names[scs.index(max(scs))]
    scwtd = max(scs)
    nls = [t1nl, t2nl,t3nl]
    nl_img = img_srcs[nls.index(max(nls))]
    nlwt = team_names[nls.index(max(nls))]
    nlwtd = max(nls)

    # 我要猜
    rts = SurveyObs.objects.filter(survey__is_valid=True).values_list('species_name', flat=True)
    total_species = len(set([re.sub(r' ?\(.*?\)','',s) for s in rts]))
    total_count = sum(SurveyObs.objects.filter(survey__is_valid=True).values_list('amount', flat=True))    
    df = pd.DataFrame.from_records(PredictionData.objects.all().values('participant_name','guess_n_species','guess_total_individual'))
    df['tsrd'] = (df.guess_n_species - total_species).tolist()
    df['abs_tsrd'] = [abs(i) for i in df.tsrd]
    df['tcrd'] = (df.guess_total_individual - total_species).tolist()
    df['abs_tcrd'] = [abs(i) for i in df.tcrd]
    ts = df.sort_values(by=['abs_tsrd']).participant_name.tolist()[:10]
    tsd = [f'+{i}' if i > 0 else f'-{i}' for i in df.sort_values(by=['abs_tsrd']).tsrd.tolist()[:10]]
    tc = df.sort_values(by=['abs_tcrd']).participant_name.tolist()[:10]
    tcd = [f'+{i}' if i > 0 else f'-{i}' for i in df.sort_values(by=['abs_tcrd']).tcrd.tolist()[:10]]

    guess_result = [
        dbc.Col([
            html.H1('最終數值:'),
            html.H3(f'總鳥種數： {total_species}',className='ml-5'),
            html.H3(f'總鳥隻數： {total_count}',className='ml-5'),
        ],width=4,style={'text-align':'left'}),
        dbc.Col([
            html.H1('預測鳥種數最接近：'),
            html.H3(f'(1) {ts[0]} ({tsd[0]})',className='ml-5'),
            html.H3(f'(2) {ts[1]} ({tsd[1]})',className='ml-5'),
            html.H3(f'(3) {ts[2]} ({tsd[2]})',className='ml-5'),
            html.H3(f'(4) {ts[3]} ({tsd[3]})',className='ml-5'),
            html.H3(f'(5) {ts[4]} ({tsd[4]})',className='ml-5'),
            html.H3(f'(6) {ts[5]} ({tsd[5]})',className='ml-5'),
            html.H3(f'(7) {ts[6]} ({tsd[6]})',className='ml-5'),
            html.H3(f'(8) {ts[7]} ({tsd[7]})',className='ml-5'),
            html.H3(f'(9) {ts[8]} ({tsd[8]})',className='ml-5'),
            html.H3(f'(10) {ts[9]} ({tsd[9]})',className='ml-5'),
        ],width=4,style={'text-align':'left'}),
        dbc.Col([
            html.H1('預測鳥隻數最接近：'),
            html.H3(f'(1) {tc[0]} ({tcd[0]})',className='ml-5'),
            html.H3(f'(2) {tc[1]} ({tcd[1]})',className='ml-5'),
            html.H3(f'(3) {tc[2]} ({tcd[2]})',className='ml-5'),
            html.H3(f'(4) {tc[3]} ({tcd[3]})',className='ml-5'),
            html.H3(f'(5) {tc[4]} ({tcd[4]})',className='ml-5'),
            html.H3(f'(6) {tc[5]} ({tcd[5]})',className='ml-5'),
            html.H3(f'(7) {tc[6]} ({tcd[6]})',className='ml-5'),
            html.H3(f'(8) {tc[7]} ({tcd[7]})',className='ml-5'),
            html.H3(f'(9) {tc[8]} ({tcd[8]})',className='ml-5'),
            html.H3(f'(10) {tc[9]} ({tcd[9]})',className='ml-5'),
        ],width=4,style={'text-align':'left'}),        
    ]


    return [t1sn, t1sc, t1nl, t2sn, t2sc,\
        t2nl, t3sn, t3sc, t3nl, pw1, pw2, pw3, \
        pw1d, pw2d, pw3d, sn_img, snwt, snwtd, \
        sc_img, scwt, scwtd, nl_img, nlwt, nlwtd, guess_result]



# @app.callback(
#     [Output('page0','style'),
#     Output('page1','style'),
#     Output('page2','style'),
#     Output('page3','style'),
#     Output('page4','style'),],
#     [Input('Bg_btn','n_clicks')], 
#     prevent_initial_call = True
# )
# def Update_Page(nc):
#     global page_index    
#     all_none = [{'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}]
#     '''
#     if works like a fucking idiot in server...
#     so I code this silly way, if I can fix it up?
#     '''
#     if page_index == 0:
#         page_index = 1
#     elif page_index == 1:
#         page_index = 2
#     elif page_index == 2:
#         page_index = 3
#     elif page_index == 3:
#         page_index = 4        
#     all_none[page_index] = {'display':'block'}
#     return all_none