# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import requests
import re
import json
import numpy
import pprint

url = 'http://localhost:42135'
#url = 'http://10.190.76.108'

pp = pprint.PrettyPrinter(indent=4)
'''
payload = {"device": [{"command": "enumerate"}]}
r = requests.post(url, json=payload)
pp.pprint(r.json())
'''

app = dash.Dash()

app.layout = html.Div([
    html.Section([],className='header'),
    html.H1(children='Dash'),
    html.Div(children='A web application framework for Python.'),
    html.Hr(),
	dcc.Graph(id='example-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000 # in milliseconds
    )
], className='container')

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(Output('example-graph', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_live():
    data = {'time': [],'voltage': []}
    '''
    payload = {"awg":{"1":[{"command":"stop"},
                           {"command":"setRegularWaveform",
                            "signalType":"square",
                            "signalFreq":1000000,
                            "vpp":3000,
                            "vOffset":0},
                           {"command":"run"}]}}
    r = requests.post(url, json=payload)
    '''
    payload = {"trigger":{"1":[{"command":"single"}]}}
    r = requests.post(url, json=payload)
    
    payload = {'osc': {'1': [{'command': 'read', 'acqCount': 1}]}}
    r = requests.post(url, json=payload)
    result = re.split(b'\r\n',r.content)
    # Decode UTF-8 bytes to Unicode, and convert single quotes 
    # to double quotes to make it valid JSON

    if len(result) > 1 and result[1]:
        str_json = result[1].decode('ASCII').replace("'", '"')
        # Load the JSON to a Python list & dump it back out as formatted JSON
        my_json = json.loads(str_json)
        #pp.pprint(my_json)

        actualSampleFreq = my_json['osc']['1'][0]['actualSampleFreq']/1000

        for i in range(0, len(result[4])-2, 2):
            data['voltage'].append(int.from_bytes(result[4][i:i+2], byteorder='little', signed=True))
            data['time'].append(i/2/actualSampleFreq)

        # Create the graph 
        return {
            'data': [go.Scatter(
                x=data['time'],
                y=data['voltage'],
                mode='lines',
            )],
            'layout': go.Layout(
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            )
        }
    else:
        print('Error reading')

if __name__ == '__main__':
    app.run_server(debug=True)
