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
T0 = '202020202020'
T1 = 'EBIRD TAIWAN'
T2 = 'FALL CHALLENGE'

string_seq = list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')
num_seq = list('012')
T0_delays = [0]
for s in T0:
    T0_delays.append(num_seq.index(s)+T0_delays[-1])
T1_delays = [0]
for s in T1:
    T1_delays.append(string_seq.index(s)+T1_delays[-1])
T2_delays = [0]
for s in T2:
    T2_delays.append(string_seq.index(s)+T2_delays[-1])

N_species_1 = 10
N_species_2 = 15
N_species_3 = 9

try:
    homepage_data = HomePage.objects.all()[0]
    team1_name = homepage_data.team1_name
    team2_name = homepage_data.team2_name
    team3_name = homepage_data.team3_name
except:
    print('data not exist in data base??')
    team1_name = '???'
    team2_name = '???'
    team3_name = '???'

def SingleTextAnim(delta_time, height_offset = 0,finished=False, target_string='Z', change_text=False, numbers = False):
    STAS = {
        "display":"inline-block",
        "width":"5rem",
        "font-size": "5rem",
        "text-align": "center",        
        }    

    if change_text and delta_time > 0:
        if numbers:
            I = num_seq.index(target_string)
        else:
            I = string_seq.index(target_string)
        STAS["color"]="rgba(0,0,0,1)"
        if delta_time >= I:
            return html.Div(target_string, style=STAS)
        return html.Div(string_seq[delta_time], style=STAS)
    

    STAS["color"]="rgba(0,0,0,0.2)"
    
    Z = 1/(1 + np.exp(-((delta_time)%10 - 5))) # use simoid function to interpolate transition
    STAS['transform'] = f"translate(0px, {Z * -25 + height_offset}px)"

    s = list("20")[int((delta_time+height_offset)/10)%2]
    if finished:
        s = target_string
        STAS['transform'] = f"translate(0px, 0px)"
    return html.Div(s,style=STAS)

def TextAnimation(delta_time, finished_time):
    s = "20"
    f = (delta_time >= finished_time)
    y_offset = 10

    sentence0 = []
    for i in range(len(T0)):
        sentence0.append(SingleTextAnim(delta_time-T0_delays[i], i%2*y_offset, f, T0[i], True, True))
    for i in range(len(T0),24):
        sentence0.append(SingleTextAnim(delta_time, i%2*y_offset, f, s[i%2]))

    sentence1 = []
    for i in range(len(T1)):
        sentence1.append(SingleTextAnim(delta_time-T1_delays[i], i%2*y_offset, f, T1[i], True))
    for i in range(len(T1),24):
        sentence1.append(SingleTextAnim(delta_time, i%2*y_offset, f, s[i%2]))
    
    sentence2 = []
    for i in range(len(T2)):
        sentence2.append(SingleTextAnim(delta_time-T2_delays[i], i%2*y_offset, f, T2[i], True))
    for i in range(len(T2),24):
        sentence2.append(SingleTextAnim(delta_time, i%2*y_offset, f, s[i%2]))

    return html.Div([
        html.Div(sentence0),
        html.Div(sentence1),
        html.Div(sentence2),         
    ],style={"transform": "rotate(-4.29deg)", "top":"130px", "position":"relative","white-space":"nowrap"})    


# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],update_title=None)
app = DjangoDash(
    'HomePage', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash



app.layout = html.Div([
    html.Div([
        html.Div([],id='bg_anim'),
    ], id='bg-overlay'),
    html.Div(id='bottom_bar'),
    dcc.Location(id='url', refresh=True),
    dcc.Interval(id='tick',interval=50,n_intervals=0),
    dcc.Interval(id='bar_update',interval=10000,n_intervals=0)
])

@app.callback(
    # [
    Output('tick', 'n_intervals'),
    # Output('bottom_bar', 'children')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    global N_species_1
    global N_species_2
    global N_species_3
    N_species_1 = 1
    N_species_2 = 1
    N_species_3 = 1
    print('is g var reeset??', N_species_1)
    # init_sb_content = [
    #     html.Div(html.P('{team1_name}紀錄到(0種)', style={"color":"#fff"}),className="score_bar", style={"width":"33%","background":"red"}),
    #     html.Div(html.P('{team2_name}紀錄到(0種)', style={"color":"#fff"}),className="score_bar", style={"width":"34%","background":"green"}),
    #     html.Div(html.P('{team3_name}紀錄到(0種)', style={"color":"#fff"}),className="score_bar", style={"width":"33%","background":"blue"})
    # ]
    return 0
    # , init_sb_content

@app.callback(
    [Output('bg_anim', 'children'),
    Output('tick', 'disabled')],
    [Input('tick','n_intervals'),]
)
def text_animation(delta_time):
    fin_ticks = 120    
    if delta_time >= fin_ticks:
        return TextAnimation(delta_time, fin_ticks), True
    
    return TextAnimation(delta_time, fin_ticks) , False

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

    s1 = f'{team1_name}紀錄到({N_species_1}種)'
    s2 = f'{team2_name}紀錄到({N_species_2}種)'
    s3 = f'{team3_name}紀錄到({N_species_3}種)'
    return [
        html.Div(html.P(s1, style={"color":"#fff"}),className="score_bar", style={"width":f"{P[0]}%","background":"red"}),
        html.Div(html.P(s2, style={"color":"#fff"}),className="score_bar", style={"width":f"{P[1]}%","background":"green","left":f"{P[0]}%"}),
        html.Div(html.P(s3, style={"color":"#fff"}),className="score_bar", style={"width":f"{P[2]}%","background":"blue","left":f"{P[0]+P[1]}%"})
    ]
    
    

if __name__ == '__main__':
    app.run_server(debug=True)