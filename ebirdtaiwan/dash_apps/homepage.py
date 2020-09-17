import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import dash_table

import plotly.graph_objs as go

import pandas as pd
import random
import numpy as np

from home.models import HomePage


'''
GLOBAL VARS

no need to declare and calculate global parameters in tick...
'''

N_species_1 = 10
N_species_2 = 15
N_species_3 = 9

homepage_data = HomePage.objects.all()[0]

team1_color = '#fff'
team2_color = '#fff'
team3_color = '#fff'

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],update_title=None)
app = DjangoDash(
    'HomePage', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash



app.layout = html.Div([
    html.Div(id='bottom_bar'),
    dcc.Location(id='url', refresh=True),
    dcc.Interval(id='tick',interval=50,n_intervals=0),
    dcc.Interval(id='bar_update',interval=10000,n_intervals=0)
])

@app.callback(
    Output('tick', 'n_intervals'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    global N_species_1
    global N_species_2
    global N_species_3    
    N_species_1 = 1
    N_species_2 = 1
    N_species_3 = 1

    for i in range(1,4):
        code_string = f'''
try:        
    team{i}_color = homepage_data.team{i}_color
except:            
    team{i}_color = '#fff'            
        '''
    exec(code_string)


    return 0


@app.callback(
    Output('bottom_bar', 'children'),
    [Input('bar_update','n_intervals')]
)
def update_species_accumulation(delta_time):
    print('is update called whenever relaod page??')
    global N_species_1
    global N_species_2
    global N_species_3
    N_species_1 += random.randint(0, 2)
    N_species_2 += random.randint(0, 3)
    N_species_3 += random.randint(0, 4)
    total = N_species_1 + N_species_2 + N_species_3
    P = [0, 0, 0]
    if total == 0:
        P = [33, 34, 33]
        
    else:
        P[0] = round(N_species_1*100/total)
        P[1] = round(N_species_2*100/total)
        P[2] = 100 - P[0] - P[1]

    # # to fix total width > 100 for some value == 0, to triger whole bar invisible
    # P[P.index(min(P))] += 1
    # P[P.index(max(P))] -= 1

    # #still some special case 0 , 0, 100 may trigger this bug

    team1_color = homepage_data.team1_color
    team2_color = homepage_data.team2_color
    team3_color = homepage_data.team3_color

    return [
        html.Div(className="score_bar", style={"width":f"{P[0]}%","background":team1_color}),
        html.Div(className="score_bar", style={"width":f"{P[1]}%","background":team2_color,"left":f"{P[0]}%"}),
        html.Div(className="score_bar", style={"width":f"{P[2]}%","background":team3_color,"left":f"{P[0]+P[1]}%"})
    ]
    
    

if __name__ == '__main__':
    app.run_server(debug=True)


'''

    地圖顏色：
1. 可以放底圖的話，設定黑色邊，不填色
2. 不可放的話，設定黑色邊，家燕（2E92D3）、彩鷸（EF8018）、大冠鷲（FFF101）
'''
