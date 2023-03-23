import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
from components import header
from components import filter

### TODO: move data load and parsing in different script
data = (
    pd.read_json('watch-history.json', convert_dates=["time"])
    .assign(date=lambda data: pd.to_datetime(data["time"], format="%Y-%m-%d"))
    .sort_values(by="date")
)

data['date']= data['date'].dt.strftime('%m-%d-%Y')
ads = data.count()["details"]
total = data.count()["title"] - ads
data_f = data[["date","title"]]
###


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
#fig1.update_traces(texttemplate="%{text:.2s}") #text formart

layout = html.Div(
    children=[
        dbc.Row(header.header()),
        html.P(
            children=(
                "Analysis of Personal Youtube History"
            ),
        ),
        html.Hr(),
        filter.filter_by_date(),
        dbc.Row(
            children=[
                dbc.Col(
                    dash_table.DataTable(
                        data=data_f.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in data_f.columns],
                        id='tbl',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'whiteSpace': 'normal'
                        })),
                dbc.Col(dcc.Graph(id="my_graph",figure=fig1))
            ]
        )
    ]
)
