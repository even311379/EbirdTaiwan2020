import dash
import dash_html_components as html
import visdcc
from dash.dependencies import Input, Output, State

app = dash.Dash()

app.layout = html.Div([
    html.Button('open url', id = 'button'),
    visdcc.Run_js(id = 'javascript')
])
           
@app.callback(
    Output('javascript', 'run'),
    [Input('button', 'n_clicks')])
def myfun(x): 
    if x: 
        return "window.open('https://yahoo.com/')"
    return ""

if __name__ == '__main__':
    app.run_server()