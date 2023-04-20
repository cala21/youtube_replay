import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from components import header, uploader

layout = html.Div(
    children=[
        dbc.Row(header.header()),
        html.P(
            children=(
                "Analysis of Personal Youtube History"
            ),
        ),
        html.Hr(),
        html.Div(children=[html.P(children=
                                  ['Upload your \'watch_history.json\' file from Google Takeout. ', 
                                    html.A('(See How?)', href='/help-page'),

                                    html.Br(),
                                    'It may take a few seconds for the data to be uploaded, parsed and loaded. Please wait for the loader to disappear and do not refresh in the middle!'])]),
    
        uploader.uploader()
    ]
)
