import base64
from datetime import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from components import header, uploader, filter
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

class Utils:

    def __init__(self):
        self.data = []

    def parse_contents(self, contents, filename, date):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                # Assume that the user uploaded an excel file
                self.data  = (
                    pd.read_json(io.BytesIO(decoded), convert_dates=["time"])
                    .assign(date=lambda data: pd.to_datetime(data["time"], format="%B %d, %Y"))
                    .sort_values(by="date")
                )
                self.data.set_index('date')
                self.data['date']= self.data['date'].dt.strftime('%B %d, %Y')
                self.data_f = self.data[["date","title"]]
            else:
                return html.Div([
                    'The file should be in json format'
                ])
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            filter.filter_by_date(),
            dbc.Row(
                children=[
                    dbc.Col(
                        dash_table.DataTable(
                            data=self.data_f.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in self.data_f.columns],
                            id='history-table',
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'height': 'auto',
                                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                'whiteSpace': 'normal'
                            })),
                    dbc.Col(dcc.Graph(id="my_graph",figure=self.load_graph()))
                ]
            ),
            html.Hr(),
            # TODO: remove, just for debugging
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])
    
    def load_graph(self):
        ads = self.data.count()["details"]
        total = self.data.count()["title"] - ads

        trace1 = go.Bar(    #setup the chart for Resolved records
            x=["Ads", "Videos"], #x for Resolved records
            y=[ads,total],#y for Resolved records
            marker_color=px.colors.qualitative.Dark24[0],  #color
            textposition="outside", #text position
            name="Resolved", #legend name
        )
        layout = go.Layout(barmode="group", title="Resolved vs Unresolved") #define how to display the columns
        fig1 = go.Figure(data=trace1, layout=layout)
        fig1.update_layout(
            title=dict(x=0.5), #center the title
            xaxis_title="Type",#setup the x-axis title
            yaxis_title="Count", #setup the x-axis title
            margin=dict(l=20, r=20, t=60, b=20),#setup the margin
            paper_bgcolor="aliceblue", #setup the background color
        )

        return fig1
    
    def filter_by_date_range(self, start, stop):
        if start is not None and stop is not None:
            return (self.data_f[(pd.to_datetime(self.data_f["date"], format="%B %d, %Y") > datetime.strptime(start, "%B %d, %Y")) \
                   & (datetime.strptime(stop, "%B %d, %Y") > pd.to_datetime(self.data_f["date"], format="%B %d, %Y"))]).to_dict('records')
        
        return self.data_f.to_dict('records')