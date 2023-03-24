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
        uploader.uploader()
    ]
)
