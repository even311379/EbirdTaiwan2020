import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import dash_table
import dash_daq as daq
import pandas as pd
import numpy as np
import json

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
mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'

def draw_ac_map(team):
    '''
    add more code a get team data
    '''
    with open('../helper_files/TaiwanCounties_simple.geojson') as f:
        geoj = json.load(f)

    data = pd.read_csv('../helper_files/TaiwanCounties.csv')    

    RN = []
    for k in range(len(geoj['features'])):
        temp = data.COUNTYNAME[k]+data.TOWNNAME[k]
        geoj['features'][k]['id'] = temp
        RN.append(temp)

    # and insert id to df
    data['Name'] = RN
    data['N_List'] = np.random.randint(0,15,len(data)).tolist()

    area_map = px.choropleth_mapbox(data, geojson=geoj, color="N_List",
                locations="Name",center={"lat": 23.9839, "lon":121.65},
                mapbox_style="stamen-terrain", zoom=8, hover_data=['Name'],                
            )
    area_map.update_traces(
        customdata=data[['Name','N_List']],
        hovertemplate='''
    <b>%{customdata[0]}</b>已上傳%{customdata[1]}份清單<extra></extra>
    ''', 
        hoverlabel=dict(font=dict(size=18)),
        marker=dict(line=dict(width=5,color='#000')),
    )
    area_map.update_layout(
        mapbox = dict(        
            accesstoken=mapbox_access_token,                        
            pitch = 45,                
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        dragmode="pan",
        coloraxis_showscale=False,
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
        # style_table={'height': f'{h}px'},
        style_table={'height': '68vh','maxHeight':'70vh'},
        id='ac_datatable'
    )


sample_card_content = [
    html.Img(src='/static/img/fall/temp_user_thumbnail.png', className='ac_card_thumbnail'),
    html.Div([html.P('王小明'), html.P('剛於xx鄉鎮上傳一份清單')],className='ac_card_content'),
    html.Div('2020/08/01 00:00:00', className='ac_card_time'),    
]



ac_map = html.Div(dcc.Graph(figure=draw_ac_map(''), id='ac_map'),id='ac_map_container')
ac_table = html.Div(draw_ac_table(), id='ac_table_container',style={'display':'none'})
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
    html.Div([
        html.Div(sample_card_content, className='ac_card'),
        html.Div(sample_card_content, className='ac_card'),
        html.Div(sample_card_content, className='ac_card'),
        html.Div(sample_card_content, className='ac_card'),
        html.Div(sample_card_content, className='ac_card'),
        html.Div(sample_card_content, className='ac_card', style={'margin-bottom':'0'}),
    ], id='ac_cards'),
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
        console.log('???')
    }
    """,
    Output('empty', 'children'),
    [Input('url', 'pathname')]
)

# '''
# should also read newest data here~~
# '''
# @app.callback(
#     Output('tt','children'),
#     [Input('empty', 'children')]
# )
# def set_size(helper_str):
#     # width = int(helper_str.split(',')[0])
#     height = int(helper_str.split(',')[1])
#     print(height)
#     print('!!??')
#     return draw_ac_table(int(height*0.7))

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

# @app.callback(
#     Output('ac_cards', 'children'),
#     [Input('tick', 'n_intervals')],
#     [State('ac_cards', 'children'),]
# )
# def TestAnimation(n_intervals, ostate):
#     if n_intervals == 10:
#         print('animation?')
#         return [
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)','opactity':'0'}),
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)'}),
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)'}),
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)'}),
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)'}),
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)'}),
#             html.Div(sample_card_content, className='ac_card',style={'transform':'translateY(-12vh)','opactity':'1'}),
#         ]
#     return [ html.Div(sample_card_content, className='ac_card',style={'transition':''}),
#             html.Div(sample_card_content, className='ac_card',style={'transition':''}),
#             html.Div(sample_card_content, className='ac_card',style={'transition':''}),
#             html.Div(sample_card_content, className='ac_card',style={'transition':''}),
#             html.Div(sample_card_content, className='ac_card',style={'transition':''}),
#             html.Div(sample_card_content, className='ac_card', style={'transition':'','margin-bottom':'0'}),
#         ]
    # return [{'transform':'translateY(-12vh)'}, {'opacity':'0','display':'none'}, {'margin-bottom':'1.5vh'}, {'opacity':'1','display':'block'}]
