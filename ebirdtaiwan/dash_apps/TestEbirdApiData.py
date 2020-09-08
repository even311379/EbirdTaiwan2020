import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import dash_table

import plotly.graph_objs as go

from ebird.api import Client
import pandas as pd
'''
add abs path from relative path to sys
in this way, I can successfully import passwords.py
'''

import sys
import os
sys.path.append(os.path.abspath('../')) 
# print(sys.path)
from automation import passwords
import datetime

mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'

region_codes = {
    'TW-TPE' : '台北',
    'TW-TPQ' : '新北',
    'TW-TAO' : '桃園',
    'TW-HSQ' : '新竹',
    'TW-MIA' : '苗栗',
    'TW-TXG' : '台中',
    'TW-CHA' : '彰化',
    'TW-NAN' : '南投',
    'TW-YUN' : '雲林',
    'TW-CYQ' : '嘉義縣',
    'TW-TNN' : '台南',
    'TW-KHH' : '高雄',
    'TW-PIF' : '屏東',
    'TW-TTT' : '台東',
    'TW-HUA' : '雲林',
    'TW-ILA' : '宜蘭',
    'TW-PEN' : '澎湖',
    'TW-KIN' : '金門',
    'TW-LIE' : '連江',
    'TW-CYI' : '嘉義市',
    'TW-KEE' : '基隆',
}

'''
There is no need to copy their data to my data base,
 just query their data is well enough
'''

df_checklist = ''


client = Client(passwords.ebird_api_key, 'zh')

def AllCheckListDashDT(date):
    
    global df_checklist

    checklists = client.get_visits('TW', date=date)
    if len(checklists) == 0:
        return html.H3(f'No data in this date: {date}')
    
    CLID     = []
    userName = []
    obsDT    = []
    county   = []
    locName  = []
    lat      = []
    lng      = []

    for checklist in checklists:
        CLID.append(checklist['subId'])
        userName.append(checklist['userDisplayName'])
        if 'obsTime' in checklist:
            obsDT.append(f'{checklist["obsDt"]} {checklist["obsTime"]}')
        else:
            obsDT.append(f'{checklist["obsDt"]} unknown time')
        if checklist['loc']['subnational1Code'] not in region_codes:
            county.append(f"??? {checklist['loc']['subnational1Code']}")
        else: 
            county.append(region_codes[checklist['loc']['subnational1Code']])                        
        locName.append(checklist['loc']['locName']) 
        lat.append(checklist['loc']['lat'])     
        lng.append(checklist['loc']['lng'])

    df_checklist = pd.DataFrame(dict(上傳清單ID=CLID,上傳使用者=userName, 紀錄日期時間=obsDT, 縣市=county, 地點名稱=locName, 緯度=lat, 經度=lng))

    df = df_checklist

    output_table = dash_table.DataTable(
        #id = table_id,
        data = df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px',
                    'font-size':'12px',
                },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_table={
                    'height':'500px'
                }
    )
    return output_table

birdcode_ref = pd.read_csv('../helper_files/eBird_Taxonomy_v2019.csv')
birdcname_ref = pd.read_csv('../helper_files/NameValid_2019.csv')

def BirdCodeToBirdCName(codestr):
    Taxa = birdcode_ref.loc[birdcode_ref.SPECIES_CODE==codestr].TAXON_ORDER.iloc[0]
    if Taxa in birdcname_ref.TAXON_ORDER.tolist():
        return birdcname_ref.loc[birdcname_ref.TAXON_ORDER==Taxa].CNAME.iloc[0]    
    return birdcode_ref.loc[birdcode_ref.SPECIES_CODE==codestr].SCI_NAME.iloc[0]


def CheckListDetailDashDT(CID):
    checklist = client.get_checklist(CID)
    if len(checklist['obs']) == 0:
        return html.H3(f'No data in this Checklist: {CID}'), html.H3(f'No data in this Checklist: {CID}')
    
    SpeciesCName = []
    howManyAtleast = []
    howManyAtmost = []
    howManyStr = []
    for obs in checklist['obs']:
        SpeciesCName.append(BirdCodeToBirdCName(obs['speciesCode']))
        howManyAtleast.append(obs['howManyAtleast'])
        howManyAtmost.append(obs['howManyAtmost'])
        howManyStr.append(obs['howManyStr'])        
        

    df = pd.DataFrame(dict(鳥名=SpeciesCName, 最少數量=howManyAtleast, 最多數量=howManyAtmost, 數量字串=howManyStr))

    output_table = dash_table.DataTable(
        data = df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_as_list_view=True,
        filter_action='native',
        sort_action='native',
        page_action='none',
        style_cell={
                    'minWidth': '30px',
                    'width': '30px',
                    'maxWidth': '30px',
                    'font-size':'12px',
                },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_table={
                    'height':'500px'
                }
    )

    lat = df_checklist.loc[df_checklist['上傳清單ID']==CID]['緯度'].iloc[0]
    lng = df_checklist.loc[df_checklist['上傳清單ID']==CID]['經度'].iloc[0]

    mapdata = [go.Scattermapbox(lat=[lat], lon=[lng],mode='markers',marker={'size':36,'symbol':'star'})]
    layout = go.Layout(autosize=True, hovermode='closest',mapbox=dict(accesstoken=mapbox_access_token,center=dict(lat=lat,lon=lng),pitch=0,zoom=12,style='outdoors'))

    output_map = dcc.Graph(figure = dict(data=mapdata, layout=layout), style={'height':'600px'})

    return output_table, output_map

app = DjangoDash(
    'TestEbirdApiData', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash

# app = dash.Dash()

# edit dash_wrapper.py 275
# "update_title = None" can only work if I modify things there

app.layout = dbc.Container([
    html.Br(),
    html.H3('資料表一'),
    html.P('從日期獲得全台灣的checklists，目前先開放兩個禮拜內的日期挑選，實際上要撈那一天都可以。'),
    html.Br(),    
    dbc.Row(
        [dbc.Col(dbc.DropdownMenu(
            label="挑選日期",
            children=[
                dbc.DropdownMenuItem((datetime.date.today()-datetime.timedelta(days=i)).strftime("%Y-%m-%d"), id=f"{i}_days_back")         
                for i in range(14)
            ], id='Dlabel'
        ), width=6),
        dbc.Col(dbc.Button("出現吧～資料～",id='Btn1',color="danger"), width=6)
        ]
    ),
    html.Br(),
    html.Div('資料尚未顯現', id='ChecklistTable'),
    html.Div(children='',id='CacheDate',style=dict(display="none")),
    html.Br(),
    html.H3('資料表二'),
    html.P('從checklist的ID獲得詳細的紀錄，需要輸入上面資料表的上傳清單ID才能看到你要的資料。'),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(dbc.Input(placeholder="輸入上傳清單ID", bs_size="lg", className="mb-3",id='ClInput'),width=6),
            dbc.Col(dbc.Button("出現吧～資料～",id='Btn2',color="danger"),width=6)
        ]
    ),
    html.Br(),
    html.H3(id='test'),
    html.Div('資料尚未顯現',id='DetailTable'),
    html.Div('地圖尚未顯現',id='Map'),
    dcc.Location(id='url', refresh=True)

])

@app.callback(
    [Output('CacheDate', 'children'),
    Output('Dlabel', 'label')],
    [Input(f'{i}_days_back', 'n_clicks') for i in range(14)])
def SyncDateState(n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", "挑選日期"
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    date_map = {f"{i}_days_back":(datetime.date.today()-datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)}
    return date_map[trigger_id], date_map[trigger_id]

@app.callback(
    Output('ChecklistTable', 'children'),
    [Input('Btn1', 'n_clicks')],
    [State('CacheDate','children')]
)
def show_datatable1(nc, date):
    if not date:
        return "資料尚未顯現"
    return AllCheckListDashDT(date)

@app.callback(
    [Output('DetailTable', 'children'),
    Output('Map','children')],
    [Input('Btn2', 'n_clicks')],
    [State('ClInput','value')]
)
def show_datatable2(nc, CLID):
    if not CLID:
        return "資料尚未顯現","資料尚未顯現"
    return CheckListDetailDashDT(CLID)

@app.callback(
    Output('Dlabel', 'children'),    
    [Input('url', 'pathname')]
)
def page_load(pathname):
    return [
        dbc.DropdownMenuItem((datetime.date.today()-datetime.timedelta(days=i)).strftime("%Y-%m-%d"), id=f"{i}_days_back")         
        for i in range(14)
    ], pathname


if __name__ == '__main__':
    app.run_server(debug=True)
