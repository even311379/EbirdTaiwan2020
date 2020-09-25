import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

import datetime

from fall.models import SignupData


teams = ['彩鷸隊','家燕隊','大冠鷲隊']


app = DjangoDash(
    'signup_summary', 
    add_bootstrap_links=True, 
)   # replaces dash.Dash

app.layout = html.Div([
    html.H1('每日新增隊員數：'),
    dcc.Graph(id='fig'),
    dcc.Location(id='url'),
    html.Div(id='empty',style={'display':'none'}),
],style={'position':'absolute', 'top':'15vh','left':'10vw','width':'80vw','height':'60vh'})


app.clientside_callback(
    """
    function(path) {
        return String(window.innerWidth) + ',' + String(window.innerHeight);
    }    
    """,
    Output('empty', 'children'),
    [Input('url', 'pathname')], prevent_initial_call = True
)

@app.callback(
    Output('fig', 'figure'),
    [Input('empty', 'children')], prevent_initial_call = True
)
def draw_on_reload(c):
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
    return f