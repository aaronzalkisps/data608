
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
#for styling
import dash_html_components as html
import chart_studio.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import flask

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
health = trees.health
#red color means the health of the Tree is poor
health[health == "Poor"] = 'rgb(255, 0, 0)'
#yellow color means the health of the Tree is fair
health[health == "Fair"] = 'rgb(255, 255, 102)'
#green color means the health of the Tree is good
health[health == "Good"] = 'rgb(0, 204, 102)'

app = dash.Dash('app', server=server)


#UI 

#reference = https://dash.plotly.com/layout
app.layout = html.Div(children=[
    #title of the application
    html.H1('Filter By Borough'), 
    
          
    dcc.Dropdown(
        id='dropdown',
        #user will be able to toggle through different boroughs
        options=[
            {'label': 'Brooklyn', 'value': 'Brooklyn'},
            {'label': 'Bronx', 'value': 'Bronx'},
            {'label': 'Manhattan', 'value': 'Manhattan'},
            {'label': 'Queens', 'value': 'Queens'},
            {'label': 'Staten Island', 'value': 'Staten Island'},
               {'label': 'All', 'value': 'All'} 
        ],
        #default selection
        value='All'
    ),
    
        html.Div (children='''Color Denotes Health of Tree'''),

    dcc.Graph(id='graph')
], className="container")

access_token = 'pk.eyJ1IjoibWljaGVsZWJyYWRsZXkiLCJhIjoiY2puaHdjdWVpMGljMDNrbzVjNW5zZTVrMSJ9.XWvfrYtiyGeHiv7K2tBO-Q'

@app.callback(Output('graph', 'figure'),
              [Input('dropdown', 'value')])
def update_graph(x):
    if x == "All":
        trees2 = trees
    else:
        trees2 = trees[trees['boroname'] == x]

    return go.Figure(
        data=Data([
            Scattermapbox(
                lat=trees2['latitude'],
                lon=trees2['longitude'],
                mode='markers',
                marker=dict(
                    size=6,
                    color = health
                ), #refer to borough column
                text=trees2['boroname'],
            ),
        ]),
        layout=Layout(
            autosize=True,
            height=750,
            hovermode='closest',
            mapbox=dict(
                accesstoken=access_token,
                bearing=0,
                center=dict(
                    lat=40.7272,
                    lon=-73.991251
                ),
                pitch=0,
                zoom=9
            ),
        )
    )
# css UI
app.css.append_css({
    'external_url': (
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/96e31642502632e86727652cf0ed65160a57497f/dash-hello-world.css'
    )
})



if __name__ == '__main__':
    app.run_server()