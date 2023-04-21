import dash_bootstrap_components as dbc
from dash import html
from components import header


layout = html.Div(
    children=[
        dbc.Row(header.header()),
        html.P(
            children=(
                "Personalized Recommendation"
            ),
        ),
        
        html.Hr(),

        html.Div(
        [
            html.Button("Get Connected User Info", id="btn-user"),
            html.Div(id="youtube-data"),
        ]),

        html.Hr(),

        html.Div(
        [
            html.Button("Get Recommended Videos for User", id="btn-rec-data"),
            html.Div(id="youtube-rec-data"),
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


