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

#create random data for test visual effect
d0 = np.zeros(len(data))
idx = np.arange(len(data))
np.random.shuffle(idx)

increment = np.append(np.random.randint(0,5,round(len(data)/4*3)),np.random.randint(3,8,round(len(data)/4)))
increment = increment.take(idx, 0)
d0 = np.vstack([d0,d0 + increment])
for i in range(29):
    increment = np.append(np.random.randint(0,5,round(len(data)/4*3)),np.random.randint(3,8,round(len(data)/4)))
    increment = increment.take(idx, 0)
    d0 = np.vstack([d0,d0[-1,:] + increment])
    
for i in range(d0.shape[0]):
    data[f'Day{i}'] = d0[i,:]

days = [f'Day{i}' for i in range(31)]

cdata = go.Choroplethmapbox(
    geojson=geoj,
    locations = data['Name'],
    customdata = data['Name'],
    z = data['Day0'],
    zmax = 150, # use these value to control color gradient
    zmin = 0,
    colorscale='Jet',
    colorbar_title='上傳清單數量',
    marker_opacity=0.5, # this can actually tune opacity
    hoverlabel=dict(font=dict(size=18)),
    name = '',
    hovertemplate="%{customdata}<extra>已累積%{z}筆清單！</extra>" 
)

clayout =go.Layout(
    title_text = 'A good title',    
    mapbox = dict(
        center=dict(lat=23.97359, lon=120.979788),
        style='carto-positron', # or 'white-bg' for empty bg
        zoom = 6,
    ),
    plot_bgcolor=None
)

clayout["updatemenus"] = [
    dict(
        type="buttons",
        buttons=[
            dict(
                label="Play",
                method="animate",
                args=[None,dict(frame=dict(duration=1000,redraw=True),fromcurrent=False)]
            ),
            dict(
                label="Pause",
                method="animate",
                args=[[None],dict(frame=dict(duration=0,redraw=True),mode="immediate")]
            )],
          direction="left",
          pad={"r": 10, "t": 35},
          showactive=False,
          x=0.1,
          xanchor="right",
          y=0,
          yanchor="top"
    )
]

sliders_dict = dict(
    active=len(days) - 1,
    visible=True,
    yanchor="top",
    xanchor="left",
    currentvalue=dict(
        font=dict(size=20),
        prefix="Date: ",
        visible=True,
        xanchor="right"),
    pad=dict(b=10,t=10),
    len=0.875,
    x=0.125,
    y=0,
    steps=[]
)

fig_frames = []
for day in days:
    frame = go.Frame(
        data=[go.Choroplethmapbox(
            locations=data['Name'],
            customdata = data['Name'],
            z=data[day],)],
         name=day)
    fig_frames.append(frame)

    slider_step = dict(
        args=[[day],
              dict(mode="immediate",
                   frame=dict(duration=3000,redraw=True))
             ],
        method="animate",
        label=day)
    sliders_dict["steps"].append(slider_step)


clayout['sliders']=[sliders_dict]
fig = go.Figure(data = cdata, layout=clayout, frames=fig_frames)

    

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div(html.Img(src='/static/img/fall/farmbird.png', className='px-3'),className='team_card_col'),
                html.Div([
                    html.Div([html.Div('隊員人數：'), html.Div('XX',className='ml-auto', id='team1_n_people')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳清單數：'),html.Div('400',className='ml-auto', id='team1_n_list')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳鳥種數:'),html.Div('544',className='ml-auto', id='team1_n_species')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳鳥隻數：'),html.Div('400',className='ml-auto', id='team1_n_count')], className='d-flex w-75'),
                ], className='bg-success team_card_col')
            ],className='bg-info single_team_card'),
            html.Div([
                html.Div(html.Img(src='/static/img/fall/citybird.png', className='px-3'),className='team_card_col'),
                html.Div([
                    html.Div([html.Div('隊員人數：'), html.Div('XX',className='ml-auto', id='team2_n_people')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳清單數：'),html.Div('400',className='ml-auto', id='team2_n_list')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳鳥種數:'),html.Div('544',className='ml-auto', id='team2_n_species')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳鳥隻數：'),html.Div('400',className='ml-auto', id='team2_n_count')], className='d-flex w-75'),
                ], className='bg-success team_card_col')
            ],className='bg-info single_team_card'),
            html.Div([
                html.Div(html.Img(src='/static/img/fall/forestbird.png', className='px-3'),className='team_card_col'),
                html.Div([
                    html.Div([html.Div('隊員人數：'), html.Div('XX',className='ml-auto', id='team3_n_people')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳清單數：'),html.Div('400',className='ml-auto', id='team3_n_list')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳鳥種數:'),html.Div('544',className='ml-auto', id='team3_n_species')], className='d-flex w-75 pb-2'),
                    html.Div([html.Div('總上傳鳥隻數：'),html.Div('400',className='ml-auto', id='team3_n_count')], className='d-flex w-75'),
                ], className='bg-success team_card_col')
            ],className='bg-info single_team_card'),           
        ],width=4),
        dbc.Col(
            dcc.Graph(figure = fig, className='prgression_map'),
            className='bg-secondary'
        ,width=8)
    ], className='bg-primary'),
    dcc.Interval(id='tick',interval=3000), # update things every 3 s for demo
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'})
    # dcc.Interval(id='tick',interval=150000), # update things every 150 s
], className='bg-danger dashboard_container')


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

@app.callback(
    Output('empty','children'),
    [Input('url','pathname')]
)
def reload_refresh(path):

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
    
    return None


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