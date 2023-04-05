import pandas as pd
import dash_bootstrap_components as dbc
from apiFacade import YoutubeHelper
from dash import dcc, html
from components import header

try:
    data = (
    pd.read_json('data/watch-history.json')
    .assign(Date=lambda data: pd.to_datetime(data["time"], format="%Y-%m-%d"))
    .sort_values(by="Date")
    )
except:
     print("An exception occurred")

layout = html.Div(
    children=[
        dbc.Row(header.header()),
        html.P(
            children=(
                "Interactive Analysis "
            ),
        ),

        html.Hr()

        # dbc.Row(
        #     children=[
        #         dbc.Row(
        #             [ 
        #                 dbc.Col(html.Div("One of three columns")),
        #                 dbc.Col(html.Div("One of three columns")),
        #                 dbc.Col(html.Div("One of three columns")),
        #             ]
        #         ),
        #         dbc.Col(dcc.Graph(id="ads-graph",figure=historyAnalysis.fig1),width=9)
        #     ]
        # )
    ]
)

'''
# Request body
yth = YoutubeHelper("dev_key")
response = yth.search()
print(response)
'''


