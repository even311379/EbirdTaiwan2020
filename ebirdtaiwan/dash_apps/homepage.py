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
import datetime

from home.models import HomePage
from fall.models import SurveyObs

'''
GLOBAL VARS

no need to declare and calculate global parameters in tick...
'''

N_species_1 = 10
N_species_2 = 15
N_species_3 = 9

homepage_data = HomePage.objects.all()[0]

team1_color = '#2E92D3'
team2_color = '#EF8018'
team3_color = '#FFF101'

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],update_title=None)
app = DjangoDash(
    'HomePage', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash

DISABLED = True

app.layout = html.Div([
    html.Div(id='bottom_bar'),
    dcc.Location(id='url', refresh=True),
    html.Div(id ='empty', style={'display':'none'})
])


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
    Output('bottom_bar','children'),
    [Input('empty', 'children')], prevent_initial_call = True
)
def hidden_graph(h):
    if datetime.date.today() < datetime.date(2020,10,1):
        return []
        # team1 = len(set(SurveyObs.objects.filter(survey__team = '黑面琵鷺隊').values_list('species_name', flat=True)))
        # team2 = 10
        # team3 = 7
    else:
        team1 = len(set(SurveyObs.objects.filter(survey__team = '彩鷸隊').values_list('species_name', flat=True)))
        team2 = len(set(SurveyObs.objects.filter(survey__team = '家燕隊').values_list('species_name', flat=True)))
        team3 = len(set(SurveyObs.objects.filter(survey__team = '大冠鷲隊').values_list('species_name', flat=True)))

    T = team1+team2+team3
    P = [round(team1*100/T), round(team2*100/T), round(team3*100/T),]
    
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
