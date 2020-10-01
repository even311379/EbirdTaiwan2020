import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import dash_table

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import random
import json
import pandas as pd
import numpy as np
import datetime
import names
import re

from fall.models import SurveyObs, Survey

import eb_passwords
from collections import Counter
'''
for team dash board

I can use pathname to deside the contents

'''


DEMO_MODE = True

app = DjangoDash(
    'OneTeam', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash


teams = ['彩鷸隊', '家燕隊', '大冠鷲隊']

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


def team_datatable(team, w):
    text_size = '1vw'
    table_height = '30vh'
    if w < 768: 
        text_size = '4vw'
        table_height = '40vh' 

    if datetime.date.today() < datetime.date(2020,10,1):
        records = SurveyObs.objects.filter(survey__team = '黑面琵鷺隊', survey__is_valid=True).values('survey__checklist_id','species_name', 'amount')
    else:
        records = SurveyObs.objects.filter(survey__team = teams[team], survey__is_valid=True).values('survey__checklist_id','species_name', 'amount')    
    df = pd.DataFrame.from_records(records)

    if len(df) == 0:
        odf = pd.DataFrame({})
    else:
        NameValidTable = pd.read_csv('../helper_files/NameValid.csv').fillna('缺值')
        CNAME = NameValidTable.CNAME.tolist()

        re_spe = []
        for s in df.species_name:
            ns = re.sub(r' ?\(.*?\)','',s)
            if s in CNAME:
                re_spe.append(s)
            elif ns in CNAME:
                re_spe.append(ns)
            else:
                re_spe.append('not valid')

        df['ValidSpecies'] = re_spe
        spe = list(set(re_spe))
        counts = []
        samples = []
        tname = []
        for s in spe:
            if s == 'not valid': continue
            counts.append(sum(df[df.ValidSpecies==s].amount))
            samples.append(len(df[df.ValidSpecies==s]))
            tname.append(s)

        odf = pd.DataFrame(dict(物種=tname,總數量=counts,清單數=samples))
        NTD = []
        TO = NameValidTable.TAXON_ORDER
        for n in tname:
            NTD.append(TO[CNAME.index(n)])
        
        odf['TO'] = NTD
        odf.sort_values(by=['TO'],inplace=True)
        odf = odf[['物種','總數量','清單數']].reset_index(drop=True)

    final_table = dash_table.DataTable(
        data = odf.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in odf.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={'minWidth': '30px','width': '30px','maxWidth': '30px','font-size':text_size,'textAlign':'center'},
        style_header={'background':'rgb(114 157 84)','color':'#fff','font-weight':'600','border':'1px solid #000','border-radius': '2vh 2vh 0 0'},
        style_data={'whiteSpace': 'normal','height': 'auto'},
        style_table={'height': table_height,'maxHeight':'70vh'},
    )

    return final_table


# prevent setup complex map twice
def empty_map():
    fig = go.Figure(go.Scattermapbox(lat=['38.91427',],lon=['-77.02827',]))
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=23.973793,lon=120.979703),
            zoom=8,
            style='white-bg')
    )
    return fig

def team_map(team, w):

    zoom = 9
    if w < 768: zoom = 8

    with open('../helper_files/TaiwanCounties_simple.geojson') as f:
        geoj = json.load(f)

    data = pd.DataFrame()

    NorthTaiwan_geo = []
    for f in geoj['features']:
        if f['properties']['COUNTYNAME'] in ['新北市', '臺北市']:
            NorthTaiwan_geo.append(f)
    geoj['features'] = NorthTaiwan_geo

    RN = []
    for k in range(len(geoj['features'])):
        temp = geoj['features'][k]['properties']['COUNTYNAME']+geoj['features'][k]['properties']['TOWNNAME']
        geoj['features'][k]['id'] = temp
        RN.append(temp)

    # and insert id to df
    data['Name'] = RN
    
    '''
    prepare the map data, the team color with most checklist in each town
    '''
    if datetime.date.today() < datetime.date(2020, 10, 1):       
        data['NC'] = np.random.randint(0, 40, len(data))
    else:
        towns = Survey.objects.filter(team=teams[team], is_valid=True).values_list('county',flat=True)
        if len(towns) == 0: return empty_map()
        county_counts = Counter(towns)
        nc = [0] * len(RN)
        for t in county_counts:
            nc[RN.index(t)] = county_counts[t]        
        data['NC'] = nc
    
    area_map = px.choropleth_mapbox(data, geojson=geoj, color="NC",
                locations="Name",center={"lat": 24.9839, "lon":121.65},
                mapbox_style="carto-positron", zoom=zoom, hover_data=['NC'],
                color_continuous_scale="Greens",                
            )
    area_map.update_traces(
        hovertemplate='%{location}  已上傳%{customdata}筆清單！<extra></extra>',        
        hoverlabel=dict(font=dict(size=16)),
        # showlegend=False,
        marker=dict(line=dict(width=1,color='#000')),
    )
    area_map.update_layout(
        mapbox = dict(        
            accesstoken=eb_passwords.map_box_api_key,                                        
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis=dict(
            colorbar = dict(
            title='上傳清單數',
            thicknessmode='fraction',
            thickness = 0.02,
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0)')),
        # this is a severe bug, dragmode = False should just remove drag, but its not working for me...  
    )

    return area_map

def draw_bar(values, names, w):

    values = values[::-1]
    names = names[::-1]
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
                    size=14),
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

def bar1_content(team, w):
    
    if datetime.date.today() < datetime.date(2020, 10, 1):
        creators = Survey.objects.filter(team='黑面琵鷺隊', is_valid=True).values_list('creator', flat=True)
    else:
        creators = Survey.objects.filter(team=teams[team]).values_list('creator', flat=True)
    ucreators = list(set(creators))
    ns = [] #number of species
    for c in ucreators:
        ns.append(len(set(SurveyObs.objects.filter(survey__creator=c, survey__is_valid=True).values_list('species_name', flat=True))))
    ns_c = sorted(zip(ns,ucreators))[::-1] #tuple of (number of species, creator)    

    return html.Div([
    dbc.Row([
        dbc.Col(html.Div('上傳鳥種數排名',className='bar_title'),md=7),        
        ],align='baseline', className='pt-2'),
    html.Hr(),
    dcc.Graph(figure=draw_bar([i[0] for i in ns_c[0:5]], [i[1] for i in ns_c[0:5]], w),config=dict(displayModeBar=False),className='bar_style'),
    html.Hr()
    ])

def bar2_content(team, w):

    if datetime.date.today() < datetime.date(2020, 10, 1):
        creators = Survey.objects.filter(team='黑面琵鷺隊', is_valid=True).values_list('creator', flat=True)
    else:
        creators = Survey.objects.filter(team=teams[team]).values_list('creator', flat=True)
    ucreators = list(set(creators))
    ta = [] #total amount
    for c in ucreators:
        ta.append(sum(SurveyObs.objects.filter(survey__creator=c, survey__is_valid=True).values_list('amount', flat=True)))
    ta_c = sorted(zip(ta,ucreators))[::-1] #tuple of (total amount, creator)    

    return html.Div([
    dbc.Row([
        dbc.Col(html.Div('上傳鳥隻數排名',className='bar_title'),md=7),        
        ],align='baseline', className='pt-2'),
    html.Hr(),
    dcc.Graph(figure=draw_bar([i[0] for i in ta_c[0:5]], [i[1] for i in ta_c[0:5]], w),config=dict(displayModeBar=False),className='bar_style'),
    html.Hr()
    ])

def bar3_content(team, w):

    if datetime.date.today() < datetime.date(2020, 10, 1):
        creators = Survey.objects.filter(team='黑面琵鷺隊', is_valid=True).values_list('creator', flat=True)
    else:
        creators = Survey.objects.filter(team=teams[team], is_valid=True).values_list('creator', flat=True)
    ucreators = list(set(creators))
    tl = [] #total list
    for c in ucreators:
        tl.append(len(Survey.objects.filter(creator=c, is_valid=True).values_list('checklist_id', flat=True)))
    tl_c = sorted(zip(tl,ucreators))[::-1] #tuple of (total amount, creator)  

    return html.Div([
    dbc.Row([
        dbc.Col(html.Div('上傳清單數排名',className='bar_title'),md=7),        
        ],align='baseline', className='pt-2'),
    html.Hr(),
    dcc.Graph(figure=draw_bar([i[0] for i in tl_c[0:5]], [i[1] for i in tl_c[0:5]], w),config=dict(displayModeBar=False),className='bar_style'),
    html.Hr()
    ])




app.layout = html.Div([
    dbc.Row([
        dbc.Col(className='img_flex_center',md=3,id='team_thumbnail'),
        dbc.Col([
            dbc.Row([
                dbc.Col(md=6, id='team_datatable'),
                dbc.Col(dcc.Graph(id='team_map',figure=empty_map(),config=dict(displayModeBar=False)),md=6),
            ],), 
            dbc.Row([
                dbc.Col(md=4, id='bar1'),
                dbc.Col(md=4, id='bar2'),
                dbc.Col(md=4, id='bar3'),
            ], className='bar_card')
        ],md=9)
    ], className=''),    
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'})
], className='dashboard_container', id='team_container')


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
    Output('team_datatable', 'children'),
    Output('team_map', 'figure'),    
    Output('bar1', 'children'),
    Output('bar2', 'children'),
    Output('bar3', 'children'),],    
    [Input('empty', 'children')], prevent_initial_call = True
)
def on_page_load(init_info):
    path = init_info.split(',')[0]
    w = int(init_info.split(',')[1])
    h = int(init_info.split(',')[2])
    
    if (path.split('/')[-2]) == 'team3':
        return team_thumbnail_content(2), team_datatable(2, w), team_map(2, w), bar1_content(2, w), bar2_content(2, w), bar3_content(2, w)
    if (path.split('/')[-2]) == 'team2':
        return team_thumbnail_content(1), team_datatable(1, w), team_map(1, w), bar1_content(1, w), bar2_content(1, w), bar3_content(1, w)
    
    return team_thumbnail_content(0), team_datatable(0, w), team_map(0, w), bar1_content(0, w), bar2_content(0, w), bar3_content(0, w)
    