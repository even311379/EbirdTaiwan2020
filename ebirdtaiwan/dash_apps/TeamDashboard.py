import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import random
import json
import pandas as pd
import numpy as np
import datetime
import names

'''
for team dash board

I can use pathname to deside the contents

'''


DEMO_MODE = True

app = DjangoDash(
    'OneTeam', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash


mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'


'''
team = 0, 1, 2
'''
def team_thumbnail_content(team):
    if team == 2:
        return html.Div([
            html.Img(src='/static/img/fall/forestbird.png', className='px-3'),
            html.H4('大冠鷲隊成績', className='text-center pt-3')
        ])
    if team == 1:
        return html.Div([
            html.Img(src='/static/img/fall/citybird.png', className='px-3'),
            html.H4('家燕隊成績', className='text-center pt-3')
        ])

    return html.Div([
            html.Img(src='/static/img/fall/farmbird.png', className='px-3'),
            html.H4('彩鷸隊成績', className='text-center pt-3')
        ])



def participants_content(team):
    '''
    need to consider lots of responsive things ...

    add more code to get participants data
    '''

    if DEMO_MODE:        
        y = [7,9,11,13,22,30,42,56,62,70,78]
        dates = [datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=i), '%Y-%m-%d') for i in range(11)]
        x = list(range(11))
        # lbs = 12

    t_info =[''] + [f'{d}: XX隊有{t}位成員囉' for t, d in zip(y,dates)]    

    y_upper = max(y) * 1.2 # hack y axis limit

    data = go.Scatter(x = x, y = y, mode='lines',line=dict(shape='spline',color='#A4B924'), name = 'ET黑面琵鷺隊', hoverinfo = 'text', text=t_info),        

    # date_text = [''] + [f'10/{i+1}' for i in range(31)]
    date_text = [''] + [f'9/{i+21}' for i in range(11)]

    # brutal force to axis...
    layout = go.Layout(
        shapes = [go.layout.Shape(type="line",x0=0,y0=0,x1=12,y1=0,line=dict(color="#000000",width=3)),
                  go.layout.Shape(type="line",x0=0,y0=0,x1=0,y1=y_upper,line=dict(color="#000000",width=3)),],
        margin=dict(l=0,r=0,b=0,t=0),
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,automargin=True,ticktext=date_text,tickvals=list(range(11)), range=[-1,13]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,automargin=True,range=[-y_upper*0.1, y_upper*1.05]),
        showlegend=False,
        dragmode = False,        
        hovermode="x",        
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[go.layout.Annotation(x=0.5,y= -y_upper*0.05,xref="paper",yref="y",text="時間",font=dict(size=16,color='#000000',family='Noto Sans TC'),showarrow=False),
            go.layout.Annotation(x=-0.5,y=0.8,xref="x",yref="paper",text="各隊累積人數",font=dict(size=16,color='#000000',family='Noto Sans TC'),showarrow=False,textangle=-90),
            go.layout.Annotation(x=12,y=0,ax=-10,ay=0,xref="x",yref="y",arrowhead=1,arrowwidth=2,arrowcolor='#000000'),
            go.layout.Annotation(x=0,y=y_upper,ax=0,ay=15,xref="x",yref="y",arrowhead=1,arrowwidth=2,arrowcolor='#000000'),]
    )

    fig = go.Figure(data=data,layout=layout)
    return dcc.Graph(figure=fig, config=dict(scrollZoom=False, displayModeBar=False), className='w-100 h-100')


def draw_bar(values, names, w):

    # for case that the total df is empty, when the chanllenge just begun, and no data can be scraped yet!
    empty_plot = False

    if len(values) == 0:
        empty_plot = True
        values= [0] * 5
        names = [''] * 5
    else:
        try:
            if len(values) < 5:
                t = [0] * (5 - len(values))
                values = t + values
                t = [' '] * (5 - len(names))
                names = t + names
        except:
            empty_plot = True
            values= [0] * 5
            names = [''] * 5

    m_names = []
    if w < 768:
        for n in names:
            c_ord = sum([ord(c) for c in n])
            if (c_ord > 40000 and len(n)> 6) or (len(n) > 15):
                if c_ord > 40000:
                    m_names.append(n[:6]+'...')
                else:
                    m_names.append(n[:12]+'...')
            else:
                m_names.append(n)
    else:
        for n in names:
            c_ord = sum([ord(c) for c in n])
            if (c_ord > 60000 and len(n)> 12) or (len(n) > 30):
                if c_ord > 40000:
                    m_names.append(n[:12]+'...')
                else:
                    m_names.append(n[:30]+'...')
            else:
                m_names.append(n)

    data = [go.Bar(x = values,
            y = [1,2,3,4,5],
            width=[0.5, 0.5, 0.5, 0.5, 0.5],
            marker_color='#5EA232',
            orientation='h',
            hoverinfo = 'text',
            hovertext = [f'{n}: {v}' for n,v in zip(names, values)]),
        go.Scatter(x = [max(values) * -0.75] * 5,
            y = [1,2,3,4,5],
            text=[f'<b>{n}</b>' for n in m_names],  # this line to fix final issue...
            mode = 'text',
            textposition="middle right",
            textfont=dict(color="black",
                family='Noto Sans TC',
                size=12,),
            hoverinfo='none'),
        ]

    # set color issue
    anno_text = [f'<b>{n}</b>' if n > 0 else ' ' for n in values]
    if not empty_plot:
        data += [go.Scatter(x = [max(values) * 0.05] * 5,
                y = [1,2,3,4,5],
                text=anno_text,
                mode = 'text',
                textposition="middle right",
                textfont=dict(
                    color='white',
                    family='Noto Sans TC',
                    size=17),
                hoverinfo='none')]

    if empty_plot:
        layout = go.Layout(
            annotations=[go.layout.Annotation(x=0.5, y=3,xref="x",yref="y",
                text="NO DATA YET!",showarrow=False,
                font=dict(family='Noto Sans TC',size=32)
            )],
            margin=dict(l=0,r=0,b=0,t=0),
            dragmode = False,
            xaxis=dict(range=[0,1],showticklabels=False,showgrid=False,zeroline=False),
            yaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
            showlegend=False,
            font=dict(family='Noto Sans TC'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',)
    else:
        layout = go.Layout(shapes = [go.layout.Shape(type="line",x0= max(values) * -0.1,x1=max(values) * -0.1,y0=1,y1=5)],
            margin=dict(l=0,r=0,b=0,t=0),
            dragmode = False,
            xaxis=dict(range=[max(values) * -0.75, max(values)],
            tickvals = [0, int(max(values) / 2), max(values)],
            showgrid=False,zeroline=False),
            yaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
            showlegend=False,
            font=dict(family='Noto Sans TC'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

    fig = go.Figure(data=data, layout=layout)

    return fig

def bar1_content(team):

    '''
    need a function to get data from db based on team
    '''
    if DEMO_MODE:
        values = np.random.randint(7,30,5)
        values.sort()

    return html.Div([
    dbc.Row([
        dbc.Col(html.Div('上傳鳥種數排名',className='bar_title'),width=7),
        dbc.Col(html.Div('1小時前更新',id='ut1',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),
        ],justify='end',align='baseline', className='pt-2'),
    html.Hr(),
    dcc.Graph(figure=draw_bar(values, [names.get_first_name() for i in range(5)], 1200), id='fNs',config=dict(displayModeBar=False),className='bar_style'),
    html.Hr()
    ], className='h-100 w-100')

def bar2_content(team):

    if DEMO_MODE:
        values = np.random.randint(400,800,5)
        values.sort()

    return html.Div([
    dbc.Row([
        dbc.Col(html.Div('上傳鳥隻數排名',className='bar_title'),width=7),
        dbc.Col(html.Div('1小時前更新',id='ut1',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),
        ],justify='end',align='baseline', className='pt-2'),
    html.Hr(),
    dcc.Graph(figure=draw_bar(values, [names.get_first_name() for i in range(5)], 1200), id='fNs',config=dict(displayModeBar=False),className='bar_style'),
    html.Hr()
    ], className='h-100 w-100')

def bar3_content(team):

    if DEMO_MODE:
        values = np.random.randint(20,70,5)
        values.sort()
    return html.Div([
    dbc.Row([
        dbc.Col(html.Div('上傳清單數排名',className='bar_title'),width=7),
        dbc.Col(html.Div('1小時前更新',id='ut1',className='text-muted', style={'text-align':'right','fontSize':12}),width=5),
        ],justify='end',align='baseline', className='pt-2'),
    html.Hr(),
    dcc.Graph(figure=draw_bar(values, [names.get_first_name() for i in range(5)], 1200), id='fNs',config=dict(displayModeBar=False),className='bar_style'),
    html.Hr()
    ], className='h-100 w-100')

def team_map(team, vh, vw):
    '''
    add more code a get team data
    '''
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
    data['N_List'] = np.random.randint(0,15,len(data)).tolist()

    area_map = px.choropleth_mapbox(data, geojson=geoj, color="N_List",
                locations="Name",center={"lat": 24.9839, "lon":121.65},
                mapbox_style="stamen-terrain", zoom=10, hover_data=['Name'],                
            )
    area_map.update_traces(
        customdata=data[['Name','N_List']],
        hovertemplate='''
    <b>%{customdata[0]}</b>已上傳%{customdata[1]}份清單<extra></extra>
    ''', 
        hoverlabel=dict(font=dict(size=18)),
        # showlegend=False,
        marker=dict(line=dict(width=5,color='#000')),
    )
    area_map.update_layout(
        mapbox = dict(        
            accesstoken=mapbox_access_token,                        
            pitch = 45,                
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        dragmode="pan",
        width=31.5*vw,
        height=37.5*vh,            
    )
    return dcc.Graph(figure=area_map)

app.layout = html.Div([
    dbc.Row([
        dbc.Col(className='w-100 h-100 img_flex_center',width=3,id='team_thumbnail'),
        dbc.Col([
            dbc.Row([
                dbc.Col(className='w-100 h-100',width=6, id='participants_curve'),
                dbc.Col(width=6, id='team_map'),
            ], className='h-50 w-100'), 
            dbc.Row([
                dbc.Col(className='h-100 w-100', width=4, id='bar1'),
                dbc.Col(className='h-100 w-100', width=4, id='bar2'),
                dbc.Col(className='h-100 w-100', width=4, id='bar3'),
            ], className='h-50 w-100 bar_card')
        ],width=9)
    ], className='h-100'),    
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'})
], className='dashboard_container')


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
    [Output('team_thumbnail', 'children'),
    Output('participants_curve', 'children'),
    Output('team_map', 'children'),    
    Output('bar1', 'children'),
    Output('bar2', 'children'),
    Output('bar3', 'children'),],    
    [Input('empty', 'children')],
    [State('team_thumbnail', 'children'),
    State('participants_curve', 'children'),
    State('team_map', 'children'),    
    State('bar1', 'children'),
    State('bar2', 'children'),
    State('bar3', 'children'),],
)
def on_page_load(init_info, stt, spc, stm, sb1, sb2, sb3):
    print(init_info)
    path = init_info.split(',')[0]
    vw = int(init_info.split(',')[1])/100
    vh = int(init_info.split(',')[2])/100
    if path == None:
        return stt, spc, stm, sb1, sb2, sb3    
    
    if (path.split('/')[-2]) == 'team3':
        return team_thumbnail_content(2), participants_content(2), team_map(2, vh, vw), bar1_content(2), bar2_content(2), bar3_content(2)
    if (path.split('/')[-2]) == 'team2':
        return team_thumbnail_content(1), participants_content(1), team_map(1, vh, vw), bar1_content(1), bar2_content(1), bar3_content(1)
    
    return team_thumbnail_content(0), participants_content(0), team_map(0, vh, vw), bar1_content(0), bar2_content(0), bar3_content(0)
    