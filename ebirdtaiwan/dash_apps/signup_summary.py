import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

import datetime

# sys.path.append(os.path.abspath('../')) 
# # print(sys.path)

from fall.models import SignupData


DEMO_MODE = False

def participants_content(team, Y):
    '''
    need to consider lots of responsive things ...

    add more code to get participants data
    '''

    if DEMO_MODE:        
        y = [7,9,11,13,22,30,42,56,62,70,78]
        dates = [datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=i), '%Y-%m-%d') for i in range(11)]
        x = list(range(11))
        # lbs = 12
    y = Y
    dates = [datetime.datetime.strftime(datetime.date(2020,9,20) + datetime.timedelta(days=i), '%Y-%m-%d') for i in range(len(Y))]
    x = list(range(len(Y)))

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

    return go.Figure(data=data,layout=layout)

teams = ['彩鷸隊','家燕隊','大冠鷲隊']

plot_data = {}

for team in teams:
    team_data = SignupData.objects.filter(team=team)
    d = datetime.date(2020,9,20)
    accd = []
    while d <= datetime.date.today():
        n = 0
        for data in team_data:            
            if data.signup_time.date() == d: n+=1
        accd.append(n)
        d = d + datetime.timedelta(days=1)
    plot_data[team] = accd


dates = []
d = datetime.date(2020,9,20)

while d <= datetime.date.today():
    dates.append(d)
    d = d + datetime.timedelta(days=1)

f = go.Figure()
for t in plot_data:
    f.add_trace(go.Scatter(x=dates, y=plot_data[t], name=t) )

# f = go.Figure([go.Scatter(x=dates, y=plot_data)])

app = DjangoDash(
    'signup_summary', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash

app.layout = html.Div([
    html.H1('每日新增隊員數：'),
    dcc.Graph(figure = f)
],style={'position':'absolute', 'top':'15vh','left':'10vw','width':'80vw','height':'60vh'})