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

from fall.models import PredictionData
'''
visdcc not working with django - dash

so.. I guess brython to write width hight to a hidden div, and then ask dash to load it...
then use convert the values to vh, vw in pixels to set all plotly graph/table/font size


brython is not working neither, can not communicate from outside scripts...

finally, there is a clientside callback in dash framework can run js...

I'll use md(768px) as the line to show my content and use viewport based unit for any possible way.

'''


prediction_df = pd.DataFrame() 

def init_df():

    global prediction_df

    if datetime.date.today() >= datetime.date(2020,10,1):
        df = pd.DataFrame.from_records(PredictionData.objects.all().values(
            'participant_name','participant_phone','guess_n_species','guess_total_individual','prediction_datetime',)
        ).sort_values(by=['prediction_datetime'])
        ns_Guess = df.guess_n_species.tolist()
        nc_Guess = df.guess_total_individual.tolist()
        prediction_df['名稱'] = df.participant_name        
        prediction_df['預測鳥種數'] = ns_Guess
        prediction_df['預測總隻數'] = nc_Guess
    else:
        ns_Guess = np.random.normal(45, 7, 80).astype(int)
        nc_Guess = ns_Guess*np.random.normal(15,2,80).astype(int) + np.random.uniform(5,30,80).astype(int)
        participant_names = [names.get_last_name() for i in range(80)]        
        prediction_df = pd.DataFrame(dict(名稱=participant_names,預測鳥種數=ns_Guess,預測總隻數=nc_Guess))
        


def empty_fig():
    fig = go.Figure()
    fig.update_layout(
        autosize = False,
        xaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False,
            showticklabels=False
        ),
        yaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False,            
            showticklabels=False
        ),
        bargap = 0,
        hovermode = 'closest',
        showlegend = False,
        dragmode=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,b=0,t=0),
    )
    return fig


def ViewportSizedHist2d(width, height):

    global prediction_df

    vw = width*45/100
    vh = height*50/100
    tw = width*0.6/100
    if width < 768:
        vw = width*80/100
        tw = width*1.5/100
    fig = go.Figure()
    fig.add_trace(go.Histogram2dContour(
            x =  prediction_df['預測鳥種數'],
            y = prediction_df['預測總隻數'],        
            colorscale = 'Greens',
            showscale =False,
            xaxis = 'x',
            yaxis = 'y',
            hoverinfo = "none",
        ))
    fig.add_trace(go.Scatter(
            x = prediction_df['預測鳥種數'],
            y = prediction_df['預測總隻數'],
            xaxis = 'x',
            yaxis = 'y',
            text = [n for n in prediction_df['名稱']],
            hoverlabel=dict(bgcolor='#000000',bordercolor='#ffffff',font=dict(size=18, color='#ffffff')),
            hovertemplate="%{text}預測，%{x}種鳥，共%{y}隻<extra></extra>", 
            mode = 'markers',
            marker = dict(
                color = '#fe7171',
                size = 3
            )
        ))
    fig.add_trace(go.Histogram(
            y = prediction_df['預測總隻數'],
            xaxis = 'x2',
            hoverinfo = "none",
            marker = dict(
                color = '#006a71'
            )
        ))
    fig.add_trace(go.Histogram(
            x = prediction_df['預測鳥種數'],
            yaxis = 'y2',
            hoverinfo = "none",
            marker = dict(
                color = '#e5df88'
            )
            
        ))

    fig.update_layout(
        autosize = False,
        xaxis = dict(zeroline = False,domain = [0,0.85],showgrid = False),
        yaxis = dict(zeroline = False,domain = [0,0.85],showgrid = False),
        xaxis2 = dict(zeroline = False,domain = [0.85,1],showgrid = False,title=dict(text='預測總鳥種數',font=dict(size=tw))),
        yaxis2 = dict(zeroline = False,domain = [0.85,1],showgrid = False,title=dict(text='預測總隻數',font=dict(size=tw))),
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

    global prediction_df

    text_size = '1vw'
    if w < 768: 
        text_size = '2vw'        
    return dash_table.DataTable(
        data = prediction_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in prediction_df.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={'minWidth': '30px','width': '30px','maxWidth': '30px','font-size':text_size,'textAlign':'center'},
        style_header={'background':'rgb(114 157 84)','color':'#fff','font-weight':'600','border':'1px solid #000','border-radius': '2vh 2vh 0 0'},
        style_data={'whiteSpace': 'normal','height': 'auto'},
    )
    

app = DjangoDash(
    'EveryonesPrediction', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash


app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4('預測鳥種數與總隻數分佈', className='dashfig_title'),
            dcc.Graph(id='hist2d', figure=empty_fig(),config=dict(displayModeBar=False),)
            ],lg=6),
        dbc.Col([
            html.H4('大家的預測', className='dashfig_title'),
            html.Div(id='predict_table'),
        ], lg=6)
    ], className='h-100'),
    html.A('我要猜',className='fall_btn teams_btn prediction_btn', href='/north_taiwan_competition/make_prediction'),        
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'}),  
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
    Output('empty', 'children'),
    [Input('url', 'pathname')]
)

'''
should also read newest data here~~
'''
@app.callback([Output('hist2d','figure'),
    Output('predict_table','children'),],
    [Input('empty', 'children')]
)
def set_size(size):
    width = int(size.split(',')[0])
    height = int(size.split(',')[1])
    init_df()
    hist2d_fig = ViewportSizedHist2d(width, height)

    return hist2d_fig, ResponsiveTable(width)
