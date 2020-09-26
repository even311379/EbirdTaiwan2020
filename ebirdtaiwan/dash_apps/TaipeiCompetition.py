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
# from fall.models import 
import plotly.express as px

import sys
import os
sys.path.append(os.path.abspath('dash_apps')) 
import CustomWidgets
import eb_passwords

'''
This is just the begining:

1. sync real data to map and numbers
2. update the map frame
3. or... remove the map layout, it's so ugly now...
4. design the hover info...

'''




DEMO_MODE = True

app = DjangoDash(
    'ThreeTeams', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

with open('../helper_files/TaiwanCounties_simple.geojson') as f:
    geoj = json.load(f)

data = pd.read_csv('../helper_files/TaiwanCounties.csv')


NorthTaiwan_geo = []
for f in geoj['features']:
    if f['properties']['COUNTYNAME'] in ['新北市', '臺北市', '基隆市']:
        NorthTaiwan_geo.append(f)
geoj['features'] = NorthTaiwan_geo
bs = [ s in ['新北市', '臺北市', '基隆市'] for s in data.COUNTYNAME]
data = data[bs].reset_index(False)

RN = []
for k in range(len(geoj['features'])):
    temp = data.COUNTYNAME[k]+data.TOWNNAME[k]
    geoj['features'][k]['id'] = temp
    RN.append(temp)

# and insert id to df
data['Name'] = RN
data['winner'] = [random.choice(['A','B','C','E']) for i in range(len(data))]


t = [random.choice(['123','456','789','555']) for i in range(len(data))]

area_map = px.choropleth_mapbox(data, geojson=geoj, color="winner",
            locations="Name",center={"lat": 24.9839, "lon":121.65},
            mapbox_style="stamen-terrain", zoom=10, hover_data=['Name'],custom_data=[data['Name']],
            color_discrete_sequence=['#2E92D3','#EF8018','#FFF101', 'rgba(255,255,255,0)'],
        )
area_map.update_traces(
    customdata=data['Name'].tolist(),
    hovertemplate='''
<b>%{customdata}</b><br><br>
<b>隊伍一</b><br>
清單數：物種數： 總隻數： <br>
<b>隊伍一</b><br>
清單數：物種數： 總隻數： <br>
<b>隊伍一</b><br>
清單數：物種數： 總隻數： 
<extra></extra>
  ''', 
    hoverlabel=dict(font=dict(size=18)),
    # showlegend=False,
    marker=dict(line=dict(width=5,color='#000')),
)
area_map.update_layout(
    mapbox = dict(        
        accesstoken=eb_passwords.map_box_api_key,                        
        pitch = 45,                
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    dragmode="pan",
    # this is a severe bug, dragmode = False should just remove drag, but its not working for me...  
)



dashboard_content = html.Div(dbc.Row([
    dbc.Col([
        html.Div([
            html.Div(html.Img(src='/static/img/fall/farmbird.png', className='px-3'),className='team_card_col'),
            html.Div([
                html.Div([html.Div('隊員人數：'), html.Div('XX',className='ml-auto', id='team1_n_people')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳清單數：'),html.Div('400',className='ml-auto', id='team1_n_list')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥種數:'),html.Div('544',className='ml-auto', id='team1_n_species')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥隻數：'),html.Div('400',className='ml-auto', id='team1_n_count')], className='d-flex w-75'),
            ], className='team_card_col')
        ],className='single_team_card'),
        html.Div([
            html.Div(html.Img(src='/static/img/fall/citybird.png', className='px-3'),className='team_card_col'),
            html.Div([
                html.Div([html.Div('隊員人數：'), html.Div('XX',className='ml-auto', id='team2_n_people')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳清單數：'),html.Div('400',className='ml-auto', id='team2_n_list')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥種數:'),html.Div('544',className='ml-auto', id='team2_n_species')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥隻數：'),html.Div('400',className='ml-auto', id='team2_n_count')], className='d-flex w-75'),
            ], className='team_card_col')
        ],className='single_team_card'),
        html.Div([
            html.Div(html.Img(src='/static/img/fall/forestbird.png', className='px-3'),className='team_card_col'),
            html.Div([
                html.Div([html.Div('隊員人數：'), html.Div('XX',className='ml-auto', id='team3_n_people')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳清單數：'),html.Div('400',className='ml-auto', id='team3_n_list')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥種數:'),html.Div('544',className='ml-auto', id='team3_n_species')], className='d-flex w-75 pb-2'),
                html.Div([html.Div('總上傳鳥隻數：'),html.Div('400',className='ml-auto', id='team3_n_count')], className='d-flex w-75'),
            ], className='team_card_col')
        ],className='single_team_card'),           
    ],width=4),
    dbc.Col(
        dcc.Graph(figure = area_map, className='prgression_map', config=dict(scrollZoom=False, displayModeBar=False)),
        className=''
    ,width=8)
]))




app.layout = html.Div([
    html.Div(dashboard_content,className='dashboard_container', id='dashboard_content',style={'display':'none'}),
    CustomWidgets.login_widget,
    CustomWidgets.leave_widget,
    dcc.Interval(id='tick',interval=3000), # update things every 3 s for demo
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'})
    ]
)


demo_t1np = 12
demo_t1nl = 63
demo_t1ns = 43
demo_t1nc = 1204
demo_t2np = 15
demo_t2nl = 53
demo_t2ns = 51
demo_t2nc = 1652
demo_t3np = 10
demo_t3nl = 70
demo_t3ns = 38
demo_t3nc = 1301


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
    [Output('dashboard_content','style'),
    Output('login_widget','style'),
    Output('leave_widget','style')],
    [Input('empty','children'),
    Input('password','value')],
)
def reload_refresh(helper_string, password_input):

    print('HEY~~')

    global demo_t1np
    global demo_t1nl
    global demo_t1ns
    global demo_t1nc
    global demo_t2np
    global demo_t2nl
    global demo_t2ns
    global demo_t2nc
    global demo_t3np
    global demo_t3nl
    global demo_t3ns
    global demo_t3nc

    demo_t1np = 12
    demo_t1nl = 63
    demo_t1ns = 43
    demo_t1nc = 1204
    demo_t2np = 15
    demo_t2nl = 53
    demo_t2ns = 51
    demo_t2nc = 1652
    demo_t3np = 10
    demo_t3nl = 70
    demo_t3ns = 38
    demo_t3nc = 1301


    if helper_string.split(',')[0].split('/')[-3] == 'private':
        if password_input == '':
            return [{'display':'none'}, {'display':'block'}, {'display':'none'}]
        elif password_input == 'iamheretotestthisapp':
            return [{'display':'block'}, {'display':'none'}, {'display':'none'}]
        else:
            return [{'display':'none'}, {'display':'none'}, {'display':'block'}]   
        
    return [{'display':'block'}, {'display':'none'}, {'display':'none'}]
    
    # return dashboard_content

# @app.callback(
#     Output('dashboard_content','children'),
#     []
# )
# def check_tester(password_input):
#     if password_input == 'iamheretotestthisapp':
#         return dashboard_content
#     return CustomWidgets.leave_widget



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
    Output('team3_n_count', 'children'),],
    [Input('tick', 'n_intervals')]    
)
def update_all_dashboard_content(tick):
    if DEMO_MODE:
        global demo_t1np
        global demo_t1nl
        global demo_t1ns
        global demo_t1nc
        global demo_t2np
        global demo_t2nl
        global demo_t2ns
        global demo_t2nc
        global demo_t3np
        global demo_t3nl
        global demo_t3ns
        global demo_t3nc

        demo_t1np += random.randint(0,2)
        demo_t1nl += random.randint(1,5)
        demo_t1ns += random.randint(0,2)
        demo_t1nc += random.randint(5,20)
        demo_t2np += random.randint(0,2)
        demo_t2nl += random.randint(1,7)
        demo_t2ns += random.randint(3,7)
        demo_t2nc += random.randint(7,35)
        demo_t3np += random.randint(0,2)
        demo_t3nl += random.randint(3,7)
        demo_t3ns += random.randint(0,2)
        demo_t3nc += random.randint(6,41)

        return demo_t1np, demo_t1nl, demo_t1ns, demo_t1nc, \
            demo_t2np, demo_t2nl, demo_t2ns, demo_t2nc, \
            demo_t3np, demo_t3nl, demo_t3ns, demo_t3nc