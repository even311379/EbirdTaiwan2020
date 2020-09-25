import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import dash_table
import dash_daq as daq

import pandas as pd
import numpy as np
import random
import json
import datetime
# from django.utils import timezone
from collections import Counter

from fall.models import AutumnChanllengeData


a = dash.Dash()
a.callback
test_data = pd.DataFrame(
    dict(
        c0=list(range(100)),
        c1=list(range(100)),
        c2=list(range(100)),
        c3=list(range(100)),
        c4=list(range(100)),
        c5=list(range(100)),
        e6=list(range(100)),
        e4=list(range(100)),
        e5=list(range(100)),
        g6=list(range(100))
    )
)



'''
initial these global variables on page loads
'''
peoples = []
towns = []
upload_time = []
thumbnail = []


# people = [names.get_first_name() for i in range(50)]
# towns = [names.get_last_name() for i in range(50)]
# sim_upload_time = [datetime.datetime(2020,10,2,14,32,38)]
# for i in range(49):
#     sim_upload_time.append(sim_upload_time[-1] + datetime.timedelta(seconds=random.randint(10,2000)))

# sim_upload_time_str = [datetime.datetime.strftime(i, '%Y-%m-%d %H:%M:%S') for i in sim_upload_time]

TEST_TIME = 0

mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'


def thumbnail_generation(seed):
    '''
    create them prior to use, just pick up one from pool, rather then generate in run time
    '''
    pass

def draw_ac_map():

    with open('../helper_files/TaiwanCounties_simple.geojson') as f:
        geoj = json.load(f)

    all_county = AutumnChanllengeData.objects.values_list('county', flat=True)
    county_counts = Counter(all_county)
    # data = pd.read_csv('../helper_files/TaiwanCounties.csv')    
    data = pd.DataFrame()

    RN = []
    for k in range(len(geoj['features'])):
        temp = geoj['features'][k]['properties']['COUNTYNAME']+geoj['features'][k]['properties']['TOWNNAME']
        geoj['features'][k]['id'] = temp
        RN.append(temp)

    # and insert id to df
    data['Name'] = RN
    
    occupied = []
    for t in RN:
        if t in county_counts:
            if county_counts[t] > 1:
                occupied.append('熱門地帶')
            else:
                occupied.append('剛佔領')
        else:
            occupied.append('空白地帶')

    data['occupied'] = occupied
    # print(county_counts)
    # print(data.head(6))
    # print(data['occupied'].tolist())
    '''
    TODO design hover text here
    (1) the first occupied person
    (2) total lists here
    (3) some of the peoples ??
    '''

    area_map = px.choropleth_mapbox(data, geojson=geoj, color="occupied",
                locations="Name",center={"lat": 23.973793, "lon":120.979703},
                hover_data=["occupied"],
                # featureidkey="properties.TOWNNAME",
                mapbox_style="white-bg", zoom=8,
                color_discrete_map={'空白地帶':'rgba(217,236,242, 1)', '剛佔領':'rgba(255,239,160, 1)', '熱門地帶':'rgba(172,75,28, 1)'},                
            )
    print("plotly express hovertemplate:", area_map.data[0].hovertemplate)
    area_map.update_traces(        
        hovertemplate='%{location}: %{customdata[0]}! <extra></extra>', 
        hoverlabel=dict(font=dict(size=18)),
        marker=dict(line=dict(width=1,color='#000')),
    )
    area_map.update_layout(
        mapbox = dict(        
            accesstoken=mapbox_access_token,                                        
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        dragmode="pan",
        hovermode='closest',
        # coloraxis_showscale=False,
        # showlegend = False,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01)
    )
    return area_map


'''
https://community.plotly.com/t/setting-datatable-max-height-when-using-fixed-headers/26417/5

dash_table.__version__: '4.9.0'
fixed_rows will make max height of this table 500px...
Finally, figured it out this as a bug, and solve it by set 'maxHeight' in style_table
'''

def draw_ac_table():    
    return dash_table.DataTable(
        data = test_data.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in test_data.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={'minWidth': '30px','width': '30px','maxWidth': '30px','font-size':'16px','textAlign':'center'},
        style_header={'background':'#6c7ae0','color':'#fff','font-weight':'600','border':'1px solid #000','border-radius': '2vh 2vh 0 0'},
        style_data={'whiteSpace': 'normal','height': 'auto'},
        style_table={'height': '68vh','maxHeight':'70vh'},
        id='ac_datatable'
    )

def create_card_content(img_seed, name, town_name, upload_time_str):
    return [
    html.Img(src='/static/img/fall/temp_user_thumbnail.png', className='ac_card_thumbnail'),
    html.Div([html.P(name), html.P(f'剛於{town_name}上傳清單')],className='ac_card_content'),
    html.Div(upload_time_str, className='ac_card_time'),    
]

now_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

# config=dict(displayModeBar=False)
ac_map = html.Div(dcc.Graph(figure=draw_ac_map(), id='ac_map'),id='ac_map_container')
ac_table = html.Div(id='ac_table_container',style={'display':'none'})
ac_switch = html.Div([
    html.Div(html.Div('切換至資料'), id='switch_hint'),
    daq.BooleanSwitch(id = 'switch', on = False, color='#A4D386'),
], id='switch_widget')
    


live_data_area = [ac_map,ac_table,ac_switch]


app = DjangoDash(
    'AutumnChallenge', 
    add_bootstrap_links=True, 
)  

app.layout = html.Div([
    html.Div(id='ac_cards'),
    html.Div(live_data_area, className='', id='live_data_area'),
    dcc.Interval(id='tick',interval=1000,n_intervals=0), # update things every 3 s for demo
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'}), # to write useful data to present things
], className='')


'''
salvation for my responsive....
'''
app.clientside_callback(
    """
    function(path) {
        return String(window.innerWidth) + ',' + String(window.innerHeight);
    }    
    """,
    Output('empty', 'children'),
    [Input('url', 'pathname')]
)



# '''
# should also read newest data here~~
# '''
@app.callback(
    [Output('ac_map','figure'),
    Output('ac_table_container','children'),
    Output('ac_cards', 'children')],
    [Input('empty', 'children')], prevent_initial_call = True
)
def redraw_onreload(helper_str):
    width = int(helper_str.split(',')[0])
    height = int(helper_str.split(',')[1])

    #(1) create map
    fig = draw_ac_map()

    #(2) create table
    table = draw_ac_table()

    #(3) init cards vars
    global peoples
    global towns
    global upload_time
    global thumbnail

    recent_data3 = AutumnChanllengeData.objects.filter(
        survey_datetime__gte=(datetime.datetime.now()-datetime.timedelta(hours=5))
    ).order_by('survey_datetime')
    df = pd.DataFrame.from_records(recent_data3.values('creator','county','survey_datetime'))
    # df = pd.read_sql_query(recent_data3)
    peoples = df['creator'].tolist()
    towns = df['county'].tolist()
    upload_time = [datetime.datetime.strftime(t, '%Y-%m-%d %H:%M:%S') for t in df['survey_datetime'].tolist()]
    thumbnail = [random.randint(0,48) for i in range(len(df))]
    cards_number = 7 if len(df) > 7 else len(df)
    cards = [
        html.Div(
            children = create_card_content(thumbnail[L], peoples[L], towns[L], upload_time[L]),
            className = 'ac_card',)
        for L in range(cards_number)]

    return fig, table, cards


    

@app.callback(
    [Output('ac_map_container', 'style'),
    Output('ac_table_container','style'),
    Output('switch_hint', 'children')],
    [Input('switch','on')]
)
def toggle_map_or_data(on):
    if on:
        return [dict(display='none'), dict(display='block'), html.Div('返回地圖', style=dict(color='#000'))]
    return [dict(display='block'), dict(display='none'), html.Div('顯示資料', style=dict(color='#fff'))]


##################################
#### moving card simulation ####
##################################




def moving_cards(T):
    return [
            html.Div(
                create_card_content(0, people[i], towns[i], sim_upload_time_str[i]),
                className='ac_card',
                style={'transform':'translateY(-12vh)'})
            for i in range(T,T+7)
        ]
    

def update_cards(T):
    return [
            html.Div(
                create_card_content(0, people[i], towns[i], sim_upload_time_str[i]),
                className='ac_card',
                style={'transition':'none'})
            for i in range(T,T+7)
        ]    

###################

# @app.callback(
#     Output('ac_cards', 'children'),
#     [Input('tick', 'n_intervals')],
#     [State('ac_cards', 'children'),]
# )
# def TestAnimation(n_intervals, ostate):

#     global TEST_TIME
#     if n_intervals % 5 == 0:
#         return moving_cards(TEST_TIME)
#     if n_intervals % 5 == 1:
#         TEST_TIME += 1
#         return update_cards(TEST_TIME)

#     raise PreventUpdate

'''

TODO make cards start from bottom rather than top

'''