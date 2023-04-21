from dash import dcc 
from dash import html
from dash.dependencies import Input, Output

from replayApp import app
from pages import historyAnalysis
from pages import recommendations
from pages import login
from pages import helpPage
from pages import homePage
from components import header
from callbackProvider import get_callbacks


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)

page_container = html.Div([dcc.Location(id="url"), header.header(), content])

app.layout = page_container

app.validation_layout = html.Div(
    children = [
        page_container,
        homePage.layout,
        helpPage.layout,
        historyAnalysis.layout,
        recommendations.layout,
        login.layout,
    ]
)

get_callbacks(app)
@app.callback(
    Output(
        component_id='page-content',
        component_property='children',
        ),
    [Input(
        component_id='url',
        component_property='pathname',
        )]
)

def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return homePage.layout
    elif pathname == '/help-page':
        return helpPage.layout
    elif pathname == '/history-analysis':
        return historyAnalysis.layout
    elif pathname == '/recommendations':
        return recommendations.layout
    elif pathname == '/login':
        return login.layout
    else:
        return '404'