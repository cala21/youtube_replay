from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

def uploader():
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '30px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dbc.Spinner(color="primary" , children=[
            html.Div(id='output-data-upload')
        ])
    ])