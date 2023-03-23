import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from replayApp import app
from pages import historyAnalysis
from pages import interactiveAnalysis
from components import header

page_container = html.Div(
    children=[
        dcc.Location(
            id='url',
            refresh=False,
        ),
        html.Div(id='page-content')
    ]
)

index_layout = dbc.Row(header.header())

app.layout = page_container

app.validation_layout = html.Div(
    children = [
        page_container,
        index_layout,
        historyAnalysis.layout,
        interactiveAnalysis.layout,
    ]
)

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
    if pathname == '/':
        return index_layout
    elif pathname == '/history-analysis':
        return historyAnalysis.layout
    elif pathname == '/interactive-analysis':
        return interactiveAnalysis.layout
    else:
        return '404'