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




'''
GLOBAL VARS

no need to declare and calculate global parameters in tick...
'''
T0 = '20202020'
T1 = 'EBIRDTAIWAN'
T2 = 'FALLCHANLLENGE'
string_seq = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
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


def SingleTextAnim(delta_time, height_offset = 0,finished=False, target_string='Z', change_text=False, numbers = False):
    STAS = {
        "display":"inline-block",
        "width":"96px",
        "font-size": "96px",
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
    for i in range(len(T0),20):
        sentence0.append(SingleTextAnim(delta_time, i%2*y_offset, f, s[i%2]))

    sentence1 = []
    for i in range(len(T1)):
        sentence1.append(SingleTextAnim(delta_time-T1_delays[i], i%2*y_offset, f, T1[i], True))
    for i in range(len(T1),20):
        sentence1.append(SingleTextAnim(delta_time, i%2*y_offset, f, s[i%2]))
    
    sentence2 = []
    for i in range(len(T2)):
        sentence1.append(SingleTextAnim(delta_time-T2_delays[i], i%2*y_offset, f, T2[i], True))
    for i in range(len(T2),20):
        sentence1.append(SingleTextAnim(delta_time, i%2*y_offset, f, s[i%2]))

    return html.Div([
        html.Div(sentence0),
        html.Div(sentence1),
        html.Div(sentence2),        
    ],style={"transform": "rotate(-4.29deg)", "top":"250px", "position":"relative"})    


# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],update_title=None)
app = DjangoDash(
    'HomePage', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash



app.layout = html.Div([
    html.Div([
        html.Div([],id='bg_anim'),
    ], id='bg-overlay'),
    # html.Div   
    dcc.Location(id='url', refresh=True),
    dcc.Interval(id='tick',interval=50,n_intervals=0)
])

@app.callback(Output('tick', 'n_intervals'),
              [Input('url', 'pathname')])
def display_page(pathname):    
    return 0

@app.callback(
    [Output('bg_anim', 'children'),
    Output('tick', 'disabled')],
    [Input('tick','n_intervals'),]
)
def text_animation(delta_time):
    fin_ticks = 100    
    if delta_time >= fin_ticks:
        return TextAnimation(delta_time, fin_ticks), True
    
    return TextAnimation(delta_time, fin_ticks) , False



if __name__ == '__main__':
    app.run_server(debug=True)