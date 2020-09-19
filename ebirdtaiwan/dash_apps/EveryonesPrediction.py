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

import time

'''
visdcc not working with django - dash

so.. I guess brython to write width hight to a hidden div, and then ask dash to load it...
then use convert the values to vh, vw in pixels to set all plotly graph/table/font size


brython is not working neither, can not communicate from outside scripts...

finally, there is a clientside callback in dash framework can run js...

I'll use md(768px) as the line to show my content and use viewport based unit for any possible way.

'''

'''
this is still static...

'''



def random_email_generation():
    domains = [ "hotmail.com", "gmail.com", "outlook.com", "yahoo.com"]
    str_seq = 'abcdefghigklmnopqrstuvwxy'
    num_seq = '0123456789'
    addr = random.choice(str_seq)
    for i in range(random.randint(4, 10)):
        addr+=random.choice(str_seq+num_seq)
    addr += '@'
    addr += random.choice(domains)
    return addr

def encrypt_email(email):
    s1 = email.split('@')[0]
    es = s1[0]+'O'*(len(s1)-2)+s1[-1]
    return es+'@'+email.split('@')[1]

DEMO_MODE = True

if DEMO_MODE == True:
    x = np.random.normal(45, 7, 80).astype(int)
    y = x*np.random.normal(15,2,80).astype(int) + np.random.uniform(5,30,80).astype(int)
    participant_names = [names.get_last_name() for i in range(80)]
    participant_emails = [random_email_generation() for i in range(80)]
    encrypted_emails = [encrypt_email(email) for email in participant_emails]
    prediction_df = pd.DataFrame(dict(名稱=participant_names,電子信箱=encrypted_emails,預測鳥種數=x,預測總隻數=y))

def ViewportSizedHist2d(vw, vh):
    fig = go.Figure()
    fig.add_trace(go.Histogram2dContour(
            x = x,
            y = y,        
            colorscale = 'Greens',
            xaxis = 'x',
            yaxis = 'y',
            hoverinfo = "none",
        ))
    fig.add_trace(go.Scatter(
            x = x,
            y = y,
            xaxis = 'x',
            yaxis = 'y',
            text = [n for n in participant_names],
            hoverlabel=dict(bgcolor='#000000',bordercolor='#ffffff',font=dict(size=18, color='#ffffff')),
            hovertemplate="%{text}預測，%{x}種鳥，共%{y}隻<extra></extra>", 
            mode = 'markers',
            marker = dict(
                color = '#fe7171',
                size = 3
            )
        ))
    fig.add_trace(go.Histogram(
            y = y,
            xaxis = 'x2',
            marker = dict(
                color = '#006a71'
            )
        ))
    fig.add_trace(go.Histogram(
            x = x,
            yaxis = 'y2',
            marker = dict(
                color = '#e5df88'
            )
            
        ))

    fig.update_layout(
        autosize = False,
        xaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False
        ),
        yaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False
        ),
        xaxis2 = dict(
            zeroline = False,
            domain = [0.85,1],
            showgrid = False,
            title='預測總鳥種數'
        ),
        yaxis2 = dict(
            zeroline = False,
            domain = [0.85,1],
            showgrid = False,
            title='預測總隻數'
        ),
        bargap = 0,
        hovermode = 'closest',
        showlegend = False,
        dragmode=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,b=0,t=0),
        height = vh,
        width = vw,
    )

    return fig

# prediction_fig = fig

def ResponsiveTable(w):
    vw = '45vw'
    if w < 768: vw='80vw'
    return dash_table.DataTable(
        data = prediction_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in prediction_df.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={'minWidth': '30px','width': '30px','maxWidth': '30px','font-size':'16px','textAlign':'center'},
        style_data={'whiteSpace': 'normal','height': 'auto'},
        style_table={'height':'50vh','width' :vw}
    )
    

app = DjangoDash(
    'EveryonesPrediction', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash


app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4('預測鳥種數與總隻數分佈', className='dashfig_title'),
            dcc.Graph(id='hist2d',config=dict(displayModeBar=False),)
            ],lg=6),
        dbc.Col([
            html.H4('大家的預測', className='dashfig_title'),
            html.Div(id='predict_table'),
        ], lg=6)
    ], className='h-100'),
    html.A('我要猜',className='fall_btn teams_btn prediction_btn', href='/make_prediction'),        
    dcc.Interval(id='tick',interval=1000), # update things every 3 s for demo
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'}),
    html.Div('',id='screen_size',style={'display':'none'}),     
], className='dashboard_container')

'''
salvation for my responsive....
'''
app.clientside_callback(
    """
    function(path) {
        console.log('!!??')
        return String(window.innerWidth) + ',' + String(window.innerHeight);
    }
    """,
    Output('screen_size', 'children'),
    [Input('url', 'pathname')]
)

'''
should also read newest data here~~
'''
@app.callback([Output('hist2d','figure'),
    Output('predict_table','children'),],
    [Input('screen_size', 'children')]
)
def set_size(size):
    width = int(size.split(',')[0])
    height = int(size.split(',')[1])
    hist2d_fig = ViewportSizedHist2d(width*45/100, height*50/100)
    return hist2d_fig, ResponsiveTable(width)