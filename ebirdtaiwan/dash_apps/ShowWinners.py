import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_table

import numpy as np
import pandas as pd
import datetime
import random
import numpy as np
import names

from fall.models import PredictionData, Survey, SurveyObs

app = DjangoDash(
    'ShowWinners', 
    add_bootstrap_links=True, 
) 

page0 = html.Div([
    html.Div('台北觀鳥大賽'),
    html.Div('得獎名單'),
    # html.Img(src=f'/static/img/home/home_banner.png', className='winner_bg_img')
], className='winner_title')

page1 = html.Div([
    html.Div('三隊總成績', className='winner_stitle'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/farmbird.png", top=True, className='winner_card_img'),
                html.H2('某某隊',className='card-title my-3'),
                html.Table([
                    html.Tr([html.Td('鳥種數',style={'text-align':'left'}),html.Td('99',style={'text-align':'right'})]),
                    html.Tr([html.Td('鳥隻數',style={'text-align':'left'}),html.Td('77',style={'text-align':'right'})]),
                    html.Tr([html.Td('清單數',style={'text-align':'left'}),html.Td('3115',style={'text-align':'right'})]),
                ], className='winner_table'),
                html.P(''),
                html.P(''),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/citybird.png", top=True, className='winner_card_img'),
                html.H2('某某隊',className='card-title my-3'),
                html.Table([
                    html.Tr([html.Td('鳥種數',style={'text-align':'left'}),html.Td('99',style={'text-align':'right'})]),
                    html.Tr([html.Td('鳥隻數',style={'text-align':'left'}),html.Td('77',style={'text-align':'right'})]),
                    html.Tr([html.Td('清單數',style={'text-align':'left'}),html.Td('3115',style={'text-align':'right'})]),
                ], className='winner_table'),
                html.P(''),
                html.P(''),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/forestbird.png", top=True, className='winner_card_img'),
                html.H2('某某隊',className='card-title my-3'),
                html.Table([
                    html.Tr([html.Td('鳥種數',style={'text-align':'left'}),html.Td('99',style={'text-align':'right'})]),
                    html.Tr([html.Td('鳥隻數',style={'text-align':'left'}),html.Td('77',style={'text-align':'right'})]),
                    html.Tr([html.Td('清單數',style={'text-align':'left'}),html.Td('3115',style={'text-align':'right'})]),
                ], className='winner_table'),
                html.P(''),
                html.P(''),
            ]),width=4),           
    ], className='fff'),
    # copy things from previous app
    # html.Img(src=f'/static/img/home/home_banner.png', className='winner_bg_img')
])

page2 = html.Div([
    html.Div('個人獎', className='winner_stitle'),
    html.Table([
        html.Tr([html.Td('鳥種數',style={'text-align':'left'}) ,html.Td('王小明'), html.Td('99',style={'text-align':'right'})]),
        html.Tr([html.Td('鳥隻數',style={'text-align':'left'}) ,html.Td('王小明'), html.Td('77',style={'text-align':'right'})]),
        html.Tr([html.Td('清單數',style={'text-align':'left'}) ,html.Td('王小明'), html.Td('3115',style={'text-align':'right'})]),
    ], className='winner_table2',),
    # html.Img(src=f'/static/img/home/home_banner.png', className='winner_bg_img')
])

page3 = html.Div([
    html.Div('團體獎', className='winner_stitle'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/farmbird.png", top=True, className='winner_card_img'),
                dbc.CardBody([
                    html.H1("鳥種數"),
                    html.H1("某某隊"),
                    html.H1("3552"),
                ]),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/citybird.png", top=True, className='winner_card_img'),
                dbc.CardBody([
                    html.H1("鳥隻數"),
                    html.H1("某某隊"),
                    html.H1("3552"),
                ]),
            ]),width=4),
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src="/static/img/fall/forestbird.png", top=True, className='winner_card_img'),
                dbc.CardBody([
                    html.H1("清單數"),
                    html.H1("某某隊"),
                    html.H1("3552"),
                ]),
            ]),width=4),           
    ], className='fff'),
    # html.Img(src=f'/static/img/home/home_banner.png', className='winner_bg_img')
])

page4 = html.Div([
    html.Div('猜猜樂得獎名單', className='winner_stitle'),
    dbc.Row([
        dbc.Col([
            html.H1('最終數值:'),
            html.H3('總鳥總數： 333',className='ml-5'),
            html.H3('總鳥隻數： 12333',className='ml-5'),
        ],width=4),
        dbc.Col([
            html.H1('預測鳥種數最接近：'),
            html.H3('(1) 某某某 (+7)',className='ml-5'),
            html.H3('(2) 某某某 (+7)',className='ml-5'),
            html.H3('(3) 某某某 (+7)',className='ml-5'),
            html.H3('(4) 某某某 (+7)',className='ml-5'),
            html.H3('(5) 某某某 (+7)',className='ml-5'),
            html.H3('(6) 某某某 (+7)',className='ml-5'),
            html.H3('(7) 某某某 (+7)',className='ml-5'),
            html.H3('(8) 某某某 (+7)',className='ml-5'),
            html.H3('(9) 某某某 (+7)',className='ml-5'),
            html.H3('(10) 某某某 (+7)',className='ml-5'),
        ],width=4),
        dbc.Col([
            html.H1('預測鳥隻數最接近：'),
            html.H3('(1) 某某某 (+7)',className='ml-5'),
            html.H3('(2) 某某某 (+7)',className='ml-5'),
            html.H3('(3) 某某某 (+7)',className='ml-5'),
            html.H3('(4) 某某某 (+7)',className='ml-5'),
            html.H3('(5) 某某某 (+7)',className='ml-5'),
            html.H3('(6) 某某某 (+7)',className='ml-5'),
            html.H3('(7) 某某某 (+7)',className='ml-5'),
            html.H3('(8) 某某某 (+7)',className='ml-5'),
            html.H3('(9) 某某某 (+7)',className='ml-5'),
            html.H3('(10) 某某某 (+7)',className='ml-5'),
        ],width=4),        
    ], className='fff')
    # html.Img(src=f'/static/img/home/home_banner.png', className='winner_bg_img')
])

page_index = 0

pages = [page0, page1, page2, page3, page4]

app.layout = html.Button([
    html.Div(children=pages[0], id='page_content'),
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
    Output('empty2','children'),    
    [Input('empty', 'children')], 
    prevent_initial_call = True
)
def init_pages(h):
    global page_index
    page_index = 0
    return 0

@app.callback(
    Output('page_content','children'),
    [Input('Bg_btn','n_clicks')], 
    prevent_initial_call = True
)
def Update_Page(nc):
    global page_index
    print('updatepage is called!?')
    if page_index >= len(pages) -1:
        return pages[len(pages) -1]
    page_index += 1
    return pages[page_index]