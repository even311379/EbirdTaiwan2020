import json
import pandas as pd
import plotly.express as px
import random
import plotly.graph_objs as go
import numpy as np

np.random

go.Choroplethmapbox

with open('helper_files/TaiwanCounties.geojson') as f:
    counties = json.load(f)

df = pd.read_csv("helper_files/TaiwanCounties.csv",
                   dtype={"TOWNID": str, "COUNTYNAME":str,"TOWNNAME":str})

R = []
for i in df.TOWNID.tolist():
    R.append(random.randint(0,30))


df['V'] = R

fig = px.choropleth_mapbox(df, geojson=counties, locations='TOWNNAME', color='V',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=10, center = {"lat": 23.5, "lon": 121.5},
                           opacity=1,
                           labels={'V':'the Value of Day1'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html('test.html')
# fig.show()