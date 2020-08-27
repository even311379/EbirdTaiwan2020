import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc

import plotly.graph_objs as go


import pandas as pd
import json
import numpy as np
import os


with open('../helper_files/TaiwanCounties_simple.geojson') as f:
    geoj = json.load(f)
    
data = pd.read_csv('../helper_files/TaiwanCounties.csv')


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


app = DjangoDash(
    'ChoroplethAnimationDemo', 
    add_bootstrap_links=True, 
)


app.layout = dbc.Container([
    html.Br(),
    dcc.Graph(figure = fig, style={'height':'600px'}),
    html.Br(),
])