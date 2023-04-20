import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from components import header, authorization


layout = html.Div(
    children=[
        dbc.Row(header.header()),
        html.P(
            children=(
                "Login : Page"
            ),
        ),
        html.Div(
        [
            html.Button("Connect with Google", id="btn-google"),
            html.Div(id="youtube-data"),
        ]
        )

        # html.Hr(),
        # authorization.login_button(),
        # html.Hr(),
        # authorization.login_table(),
        # authorization.logout_button()

    ]
)



'''
# Request body
yth = YoutubeHelper("dev_key")
response = yth.search()
print(response)
'''


