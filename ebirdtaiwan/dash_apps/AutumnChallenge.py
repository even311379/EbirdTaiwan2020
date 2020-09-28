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

from eb_passwords import map_box_api_key

a = dash.Dash()
a.callback
test_data = pd.DataFrame(
    dict(
        上傳人=list(range(100)),
        總清單數=list(range(100)),
        佔領鄉鎮數=list(range(100)),
        拓荒鄉鎮數=list(range(100)),
        特殊得分=list(range(100)),
        總得分=list(range(100)),
    )
)



'''
initial these global variables on page loads
'''
peoples = []
towns = []
upload_time = []
thumbnail = []
random_delay = []
CARD_POSITION = 0



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


def create_score_df():

    df = pd.DataFrame.from_records(
        AutumnChanllengeData.objects.filter(is_valid=True).values(
            'creator','survey_datetime','latitude','longitude','county',))

    creator_count = df.creator.value_counts()
    number_of_checklist = creator_count.tolist()
    unique_creator = creator_count.index.tolist()

    unique_county = pd.unique(df.county)

    number_of_occupied = [len(pd.unique(df[df.creator == c].county)) for c in unique_creator]

    first_counties = ['']*len(unique_creator)
    for county in unique_county:        
        sdf = df[df.county == county].sort_values(by=['survey_datetime'])
        # extra code tp handle shared list issue, return a list of person...
        for c in sdf[sdf.survey_datetime == sdf.survey_datetime.min()].creator.tolist():
            first_counties[unique_creator.index(c)] += county+','

    first_counties = [s[:-1] if s else '' for s in first_counties]
    first_county_numbers = [len(s.split(',')) for s in first_counties]
            
    special_score = ['']*len(unique_creator)

    north_person = df[df.latitude == df.latitude.max()].creator.iloc[0]
    south_person = df[df.latitude == df.latitude.min()].creator.iloc[0]
    east_person = df[df.longitude == df.longitude.max()].creator.iloc[0]
    west_person = df[df.longitude == df.longitude.min()].creator.iloc[0]

    special_score[unique_creator.index(north_person)] += f'極北 (緯度：{round(df.latitude.max(), 3)})'
    special_score[unique_creator.index(south_person)] += f'極南 (緯度：{round(df.latitude.min(), 3)})'
    special_score[unique_creator.index(east_person)] += f'極東 (經度：{round(df.longitude.max(), 3)})'
    special_score[unique_creator.index(west_person)] += f'極西 (經度：{round(df.longitude.min(), 3)})'


    total_score = [i + j for i,j in zip(number_of_occupied, first_county_numbers)]


    total_score[unique_creator.index(north_person)] += 5
    total_score[unique_creator.index(south_person)] += 5
    total_score[unique_creator.index(east_person)] += 5
    total_score[unique_creator.index(west_person)] += 5

    return pd.DataFrame(
        dict(
            挑戰者=unique_creator,
            總清單數=number_of_checklist,
            佔領鄉鎮數=number_of_occupied,
            首次佔領鄉鎮=first_counties,
            特殊得分=special_score,
            總得分=total_score
            )
        )


def draw_ac_map(score_df):

    with open('../helper_files/TaiwanCounties_simple.geojson') as f:
        geoj = json.load(f)

    all_county = AutumnChanllengeData.objects.values_list('county', flat=True)
    county_counts = Counter(all_county)

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


    # data['hover_text'] = occupied
    
    '''
    TODO design hover text here
    (1) the first occupied person
    (2) total lists here
    (3) some of the peoples ??
    '''
    #use score_df to do things...some what complex skip it for a few minutes
    who = ['' for i in range(len(data))]
    for p, t in zip(score_df['挑戰者'].tolist(), score_df['首次佔領鄉鎮'].tolist()):
        if not t: continue
        for town in t.split(','):
            if town == '不在台灣啦!': continue
            who[RN.index(town)] += p + ','
    who = [s[:-1] if s else '' for s in who]
    info = []

    for o, w in zip(occupied, who):
        if o == '空白地帶':
            info.append(o+'!')
        else:
            info.append(f'{o}!<br>最早占領者為 <b>{w}</b>！')

    data['info'] = info

    area_map = px.choropleth_mapbox(data, geojson=geoj, color="occupied",
                locations="Name",center={"lat": 23.973793, "lon":120.979703},
                hover_data=["info"],
                mapbox_style="white-bg", zoom=7,
                # mapbox_style="carto-positron", zoom=8,
                color_discrete_map={'空白地帶':'rgba(217,236,242, 1)', '剛佔領':'rgba(255,239,160, 1)', '熱門地帶':'rgba(172,75,28, 1)'},                
            )
    # print("plotly express hovertemplate:", area_map.data[0].hovertemplate)
    area_map.update_traces(        
        hovertemplate='%{location}: %{customdata[0]} <extra></extra>', 
        hoverlabel=dict(font=dict(size=18)),
        marker=dict(line=dict(width=1,color='#000')),
    )
    area_map.update_layout(
        mapbox = dict(        
            accesstoken=map_box_api_key,                                        
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        dragmode="pan",
        hovermode='closest',
        # coloraxis_showscale=False, 
        # showlegend = False,
        legend=dict(
            title='',
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




def draw_ac_table(score_df, v_width):

    text_size = '1vw'
    if v_width < 768: text_size = '2vw'

    return dash_table.DataTable(
        data = score_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in score_df.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={'minWidth': '30px','width': '30px','maxWidth': '30px','font-size':text_size,'textAlign':'center'},
        style_header={'background':'rgb(114 157 84)','color':'#fff','font-weight':'600','border':'1px solid #000','border-radius': '2vh 2vh 0 0'},
        style_data={'whiteSpace': 'normal','height': 'auto'},
        style_table={'height': '68vh','maxHeight':'70vh'},
        id='ac_datatable'
    )

def create_card_content(img_seed, name, town_name, upload_time_str):
    return [
    html.Img(src=f'/static/img/fall/random_thumbnails/{img_seed}.png', className='ac_card_thumbnail'),
    html.Div([html.P(name), html.P(f'在 {town_name} 上傳')],className='ac_card_content'),
    html.Div(upload_time_str, className='ac_card_time'),    
]


ac_map = html.Div(dcc.Graph(figure=empty_map(), id='ac_map', config=dict(displayModeBar=False)),id='ac_map_container')
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
    html.Div(live_data_area, id='live_data_area'),
    # dcc.Interval(id='tick',interval=1000,n_intervals=0),
    dcc.Location(id='url'),
    html.Div('',id='empty',style={'display':'none'}), # to write useful data to present things
])


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
    Output('ac_table_container','children')],
    # Output('tick', 'n_intervals')],
    [Input('empty', 'children')], prevent_initial_call = True
)
def redraw_onreload(helper_str):
    width = int(helper_str.split(',')[0])
    # height = int(helper_str.split(',')[1])    
    global CARD_POSITION

    #(1) create score data_frame
    score_df = create_score_df()
    
    #(2) create map
    fig = draw_ac_map(score_df)

    #(3) create table
    table = draw_ac_table(score_df, width)    

    CARD_POSITION = 0

    return fig, table    

@app.callback(
    [Output('ac_map_container', 'style'),
    Output('ac_table_container','style'),
    Output('switch_hint', 'children'),
    ],
    [Input('switch','on')]
)
def toggle_map_or_data(on):
    if on:
        return [dict(display='none'), dict(display='block'), html.Div('返回地圖', style=dict(color='#000'))]
    return [dict(display='block'), dict(display='none'), html.Div('顯示資料', style=dict(color='#000'))]
