import base64
from datetime import datetime
from  dateutil import parser
import io

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from components import header, uploader, filter
import plotly.express as px
import plotly.graph_objects as go
from apiFacade import YoutubeHelper

import pandas as pd

class Utils:

    def __init__(self):
        self.data = []
        self.yth = YoutubeHelper("<API_KEY>")

    #region Youtube API data cleaning
    
    def clean_video_details(self):
        # Extract ids from watched history urls
        watched_videos = self.data[self.data["details"].notnull() == False]
        watched_videos = watched_videos[watched_videos["titleUrl"].notna()]
        ids = []
        categories = self.clean_categories()

        for index,video in watched_videos.iterrows():
            ids.append(video["titleUrl"].replace("?v=","/").split("watch/")[1])
            watched_videos.loc[index, "id"] = video["titleUrl"].replace("?v=","/").split("watch/")[1]

        # Limit request to 50 elements 
        # TODO: add logic to go over entire history
        ids_s = ",".join(ids[:49])
        video_data_details = self.yth.get_video_details(ids_s)
        
        data_norm = pd.json_normalize(video_data_details["items"])
        data_norm = data_norm.rename(columns={"snippet.title": "title",
                        "snippet.description": "description",
                        "contentDetails.duration": "duration",
                        "snippet.categoryId": "categoryId",
                        "statistics.viewCount": "viewCount",
                        "statistics.likeCount": "likeCount",
                        "statistics.commentCount": "commentCount"})
        data_norm = data_norm.merge(watched_videos[["id","date"]], how="left", on="id")
        data_norm['categoryName'] = data_norm.apply(lambda x: categories[x['categoryId']]["categoryName"], axis=1)

        return data_norm[["id","date","categoryName","title","description","duration","categoryId","viewCount","likeCount","commentCount"]]
    
    def clean_categories(self, location="US"):
        category_details = self.yth.get_video_category(location)
        data_norm = pd.json_normalize(category_details["items"])
        data_norm = data_norm.rename(columns={"snippet.title": "categoryName"})

        return data_norm[["id","categoryName"]].set_index("id").to_dict('index')
    #endregion

    #region Parsers
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
                self.data_cleaned = self.clean_video_details()
                # print(self.clean_video_details())
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
                    # dbc.Col(
                        # dash_table.DataTable(
                        #     data=self.data_f.to_dict('records'),
                        #     columns=[{"name": i, "id": i} for i in self.data_f.columns],
                        #     id='history-table',
                        #     style_table={'overflowX': 'auto'},
                        #     style_cell={
                        #         'height': 'auto',
                        #         'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                        #         'whiteSpace': 'normal'
                        #     })),
                    dbc.Col(
                        dcc.Graph(
                            id='crossfilter-indicator-scatter',
                            figure=self.load_scatter(self.data_cleaned)
                        )),
                    dbc.Col(dcc.Graph(id="my_graph",figure=self.load_graph(self.data)))
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
    
    def parse_date(self, start_date, end_date):
        start_date_string = None
        end_date_string = None
        if start_date is not None:
            start_date_object = parser.isoparse(start_date)
            start_date_string = start_date_object.strftime('%B %d, %Y')
        if end_date is not None:
            end_date_object = parser.isoparse(end_date)
            end_date_string = end_date_object.strftime('%B %d, %Y')
        return (start_date_string, end_date_string)

    def filter_by_date_range(self, start, stop):
        if start is not None and stop is not None:
            return (self.data[(pd.to_datetime(self.data["date"], format="%B %d, %Y") > datetime.strptime(start, "%B %d, %Y")) \
                   & (datetime.strptime(stop, "%B %d, %Y") > pd.to_datetime(self.data["date"], format="%B %d, %Y"))])
        
        return self.data
    #endregion

    #region DOM components
    def load_scatter(self, data):
        # print(data['viewCount'])
        fig = px.scatter(x=data['date'],
                y=data['viewCount'],
                hover_name=data['title']
                )

        # fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

        # fig.update_xaxes(title="Date", type='linear')

        fig.update_yaxes(title="Views", type='linear')

        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
        return fig

    def load_graph(self, data):
        ads = data.count()["details"]
        total = data.count()["title"] - ads

        trace1 = go.Bar(    #setup the chart for Resolved records
            x=["Ads", "Videos"], #x for Resolved records
            y=[ads,total],#y for Resolved records
            marker_color=px.colors.qualitative.Dark24[0],  #color
            textposition="outside" #text position
        )
        layout = go.Layout(barmode="group", title="Ads vs Watched Videos") #define how to display the columns
        fig1 = go.Figure(data=trace1, layout=layout)
        fig1.update_layout(
            title=dict(x=0.5), #center the title
            xaxis_title="Type",#setup the x-axis title
            yaxis_title="Count", #setup the x-axis title
            margin=dict(l=20, r=20, t=60, b=20),#setup the margin
            paper_bgcolor="aliceblue", #setup the background color
        )

        return fig1
    #endregion
