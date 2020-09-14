import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# from fall.models import 

# app = DjangoDash(
#     'ThreeTeams', 
#     add_bootstrap_links=True, 
# )   # replaces dash.Dash

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(),
            html.Div(),
            html.Div(),
        ],width=4),
        dbc.Col(,width=8)
    ], className='')

],fluid=True)