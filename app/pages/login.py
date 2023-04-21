import dash_bootstrap_components as dbc
from dash import html
from components import header


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
            html.Button("Get YouTube Data for User", id="btn-google", hidden=True),
            html.Div(id="youtube-data"),
        ]),

        html.Hr(),

        html.Div(
        [
            html.Button("Clear creds", id="btn-creds"),
            html.Div(id="youtube-creds-clear"),
        ]),
    ]
)



'''
# Request body
yth = YoutubeHelper("dev_key")
response = yth.search()
print(response)
'''


