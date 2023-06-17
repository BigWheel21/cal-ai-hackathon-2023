import os
from utils import get_chatbot, generate_visual_code, extract_python_code
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback


os.environ['OPENAI_API_KEY'] = ''

chat = get_chatbot()

# demo data
data = pd.DataFrame({'date':['2022/01/01','2022/01/02','2022/01/03','2022/01/04','2022/01/05'],
                     'price':[100,200,50,30,500]})

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='AI Visualizer', style={'textAlign':'center'}),
    html.Div( dcc.Textarea(id='input-on-submit',style={'width': '50%', 'height': 100, 'align':'center'}),
            style={'align':'center'}),
    html.Div(html.Button('Submit', id='submit-val', n_clicks=0),style={'align':'center'}),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    if n_clicks>0:
        res = generate_visual_code(data, value, chat)
        code = extract_python_code(res.content)
        exec(code, globals()) # the code from LLM will store the graph in the variable "fig"
        return fig
    return {}

if __name__ == '__main__':
    app.run_server(debug=False)