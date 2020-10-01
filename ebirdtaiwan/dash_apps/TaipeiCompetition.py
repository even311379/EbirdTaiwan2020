import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import random
import json
import pandas as pd
import numpy as np
import datetime
from fall.models import SignupData, Survey, SurveyObs
import plotly.express as px

import eb_passwords
from collections import Counter


DEMO_MODE = True

app = DjangoDash(
    'ThreeTeams', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash


# prevent setup complex map twice
def empty_map():
    fig = go.Figure(go.Scattermapbox(lat=['38.91427',],lon=['-77.02827',]))
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=23.973793,lon=120.979703),
            zoom=8,
            style='white-bg')
    )
    return fig


def draw_area_map():    

    with open('../helper_files/TaiwanCounties_simple.geojson') as f:
        geoj = json.load(f)

    data = pd.DataFrame()

    NorthTaiwan_geo = []
    for f in geoj['features']:
        if f['properties']['COUNTYNAME'] in ['新北市', '臺北市']:
            NorthTaiwan_geo.append(f)
    geoj['features'] = NorthTaiwan_geo

    RN = []
    for k in range(len(geoj['features'])):
        temp = geoj['features'][k]['properties']['COUNTYNAME']+geoj['features'][k]['properties']['TOWNNAME']
        geoj['features'][k]['id'] = temp
        RN.append(temp)

    # and insert id to df
    data['Name'] = RN
    
    '''
    prepare the map data, the team color with most checklist in each town
    '''
    if datetime.date.today() < datetime.date(2020, 10, 1):
        for t in ['彩鷸隊', '家燕隊', '大冠鷲隊']:
            data[t] = np.random.randint(5, 40, len(data))
    else:
        temp_town = []
        for t in ['彩鷸隊', '家燕隊', '大冠鷲隊']:
            temp_town.append(Survey.objects.filter(team=t, is_valid=True).values_list('county',flat=True))
        if not temp_town[0] and not temp_town[1] and not temp_town[2]:
            return empty_map()

        for t in ['彩鷸隊', '家燕隊', '大冠鷲隊']:
            towns = Survey.objects.filter(team=t, is_valid=True).values_list('county',flat=True)
            county_counts = Counter(towns)
            nc = [0] * len(RN)
            for k in county_counts:
                nc[RN.index(k)] = county_counts[k]        
            data[t] = nc

    winner = data[['彩鷸隊', '家燕隊', '大冠鷲隊']].idxmax(axis=1).tolist()
    
    # handles when the score are all the same
    BL = (data['彩鷸隊']==data['家燕隊']) & (data['家燕隊']==data['大冠鷲隊']) & (data['彩鷸隊']==data['大冠鷲隊'])
    for i, b in enumerate(BL):
        if b:
            winner[i] = '平手'

    data['winner'] = winner
    # data['winner'] = [random.choice(['A','B','C','E']) for i in range(len(data))]
    # t = [random.choice(['123','456','789','555']) for i in range(len(data))]

    area_map = px.choropleth_mapbox(data, geojson=geoj, color="winner",
                locations="Name",center={"lat": 24.9839, "lon":121.65},
                mapbox_style="carto-positron", zoom=10, hover_data=['彩鷸隊', '家燕隊', '大冠鷲隊'],
                color_discrete_map={'彩鷸隊':'#2E92D3', '家燕隊':'#EF8018', '大冠鷲隊':'#FFF101','平手':'rgba(255,255,255,0.3)'},                                
            )
    area_map.update_traces(
        hovertemplate='''
    <b>%{location}</b><br>
    上傳清單數<br><br>
        彩鷸隊: %{customdata[0]}<br>
        家燕隊: %{customdata[1]}<br>
        大冠鷲隊: %{customdata[2]}<extra></extra>
    ''', 
        hoverlabel=dict(font=dict(size=16)),
        # showlegend=False,
        marker=dict(line=dict(width=1,color='#000')),
    )
    area_map.update_layout(
        mapbox = dict(        
            accesstoken=eb_passwords.map_box_api_key,                                        
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            title='上傳清單數比較',
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0)'),
        # this is a severe bug, dragmode = False should just remove drag, but its not working for me...  
    )

    return area_map


dashboard_content = html.Div(dbc.Row([
    dbc.Col([
        html.Div([
            html.Div(html.Img(src='/static/img/fall/farmbird.png', className='px-3'),className='team_card_col'),
            html.Div([
                html.Div([html.Div('隊員人數：'), html.Div('',className='ml-auto', id='team1_n_people')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳清單數：'),html.Div('',className='ml-auto', id='team1_n_list')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥種數:'),html.Div('',className='ml-auto', id='team1_n_species')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥隻數：'),html.Div('',className='ml-auto', id='team1_n_count')], className='d-flex w-75'),
            ], className='team_card_col')
        ],className='single_team_card'),
        html.Div([
            html.Div(html.Img(src='/static/img/fall/citybird.png', className='px-3'),className='team_card_col'),
            html.Div([
                html.Div([html.Div('隊員人數：'), html.Div('',className='ml-auto', id='team2_n_people')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳清單數：'),html.Div('',className='ml-auto', id='team2_n_list')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥種數:'),html.Div('',className='ml-auto', id='team2_n_species')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥隻數：'),html.Div('',className='ml-auto', id='team2_n_count')], className='d-flex w-75'),
            ], className='team_card_col')
        ],className='single_team_card'),
        html.Div([
            html.Div(html.Img(src='/static/img/fall/forestbird.png', className='px-3'),className='team_card_col'),
            html.Div([
                html.Div([html.Div('隊員人數：'), html.Div('',className='ml-auto', id='team3_n_people')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳清單數：'),html.Div('',className='ml-auto', id='team3_n_list')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥種數:'),html.Div('',className='ml-auto', id='team3_n_species')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥隻數：'),html.Div('',className='ml-auto', id='team3_n_count')], className='d-flex w-75'),
            ], className='team_card_col')
        ],className='single_team_card'),           
    ], md=4),
    dbc.Col(
        dcc.Graph(figure = empty_map(),id='area_map', className='prgression_map', config=dict(displayModeBar=False)),
        className=''
    , md=8)
]))




app.layout = html.Div([
    html.Div(dashboard_content,className='dashboard_container'),
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'})
    ]
)

app.clientside_callback(
    """
    function(path) {
        console.log(path)
        return path+',' + String(window.innerWidth) + ',' + String(window.innerHeight);
    }
    """,
    Output('empty', 'children'),
    [Input('url', 'pathname')]
)


@app.callback(
    [Output('team1_n_people', 'children'),
    Output('team1_n_list', 'children'),
    Output('team1_n_species', 'children'),
    Output('team1_n_count', 'children'),
    Output('team2_n_people', 'children'),
    Output('team2_n_list', 'children'),
    Output('team2_n_species', 'children'),
    Output('team2_n_count', 'children'),
    Output('team3_n_people', 'children'),
    Output('team3_n_list', 'children'),
    Output('team3_n_species', 'children'),
    Output('team3_n_count', 'children'),
    Output('area_map','figure')],
    [Input('empty','children'),],
)
def reload_refresh(helper_string):

    t1np = len(SignupData.objects.filter(team='彩鷸隊'))
    t2np = len(SignupData.objects.filter(team='家燕隊'))
    t3np = len(SignupData.objects.filter(team='大冠鷲隊'))
    if datetime.date.today() < datetime.date(2020,10,1):
        t1nl = 63
        t1ns = 43
        t1nc = 1204
        t2nl = 53
        t2ns = 51
        t2nc = 1652
        t3nl = 70
        t3ns = 38
        t3nc = 1301
    
    else:
        t1nl = len(Survey.objects.filter(team='彩鷸隊'))
        t1ns = len(set(SurveyObs.objects.filter(survey__team = '彩鷸隊').values_list('species_name', flat=True)))
        t1nc = sum(SurveyObs.objects.filter(survey__team = '彩鷸隊').values_list('amount', flat=True))
        t2nl = len(Survey.objects.filter(team='家燕隊'))
        t2ns = len(set(SurveyObs.objects.filter(survey__team = '家燕隊').values_list('species_name', flat=True)))
        t2nc = sum(SurveyObs.objects.filter(survey__team = '家燕隊').values_list('amount', flat=True))
        t3nl = len(Survey.objects.filter(team='大冠鷲隊'))
        t3ns = len(set(SurveyObs.objects.filter(survey__team = '大冠鷲隊').values_list('species_name', flat=True)))
        t3nc = sum(SurveyObs.objects.filter(survey__team = '大冠鷲隊').values_list('amount', flat=True))

    return t1np, t1nl, t1ns, t1nc, t2np, t2nl, t2ns, t2nc, t3np, t3nl, t3ns, t3nc, draw_area_map()
