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
from collections import defaultdict
import numpy as np
import warnings; warnings.filterwarnings("ignore")

import pandas as pd

# Added for word cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

class Utils:

    def __init__(self):
        self.data = []
        self.yth = YoutubeHelper("API_KEY")


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

        data_norm = pd.DataFrame()
        for i in range(0,len(ids)-50,50):
        # for i in range(0,100,50):
            ids_s = ",".join(ids[i+1:i+50])
            video_data_details = self.yth.get_video_details(ids_s)
            data_norm = pd.concat([data_norm, pd.json_normalize(video_data_details["items"])])

        ids_s = ",".join(ids[i+1:i+np.mod(len(ids),50)])
        video_data_details = self.yth.get_video_details(ids_s)
        data_norm = pd.concat([data_norm, pd.json_normalize(video_data_details["items"])])
        data_norm = data_norm.rename(columns={"snippet.title": "title",
            "snippet.description": "description",
            "contentDetails.duration": "duration",
            "snippet.categoryId": "categoryId",
            "statistics.viewCount": "viewCount",
            "statistics.likeCount": "likeCount",
            "statistics.commentCount": "commentCount"})
        data_norm = data_norm.merge(watched_videos[["id","date"]], how="left", on="id")
        data_norm['categoryName'] = data_norm.apply(lambda x: categories[x['categoryId']]["categoryName"], axis=1)
        data_norm.sort_index(inplace=True)

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
                self.data  = (
                    pd.read_json(io.BytesIO(decoded), convert_dates=["time"])
                    .assign(date=lambda data: pd.to_datetime(data["time"], format="%B %d, %Y"))
                    .sort_values(by="date")
                )
                self.data.set_index('date')
                self.data_cleaned = self.clean_video_details()
                self.data_with_ads = self.data[["date","title"]]
            else:
                return html.Div([
                    'The file should be in json format'
                ])
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        
        cloud = self.load_word_cloud(self.data_cleaned)
        return html.Div([
                filter.filter_by_date(self.data['date'].min(), self.data['date'].max()),
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
                            id='views-scatter',
                            figure=self.load_scatter(self.data_cleaned)
                        )),
                    dbc.Col(
                        dcc.Graph(
                            id="ads-graph",
                            figure=self.load_graph(self.data)
                        ))
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        dcc.Graph(
                            id='genre-graph',
                            figure=self.load_genre_graph(self.data_cleaned)
                        )),
                    dbc.Col(
                        dcc.Graph(
                            id='time-graph',
                            figure=self.load_time_trend_graph(self.data_cleaned)
                        ))
                ]
            ),
            # dbc.Row(
            #     children=self.load_word_cloud(self.data_cleaned)
            # ),
            dbc.Row(
                dbc.Col([
                    html.Img(id='word-cloud', src=cloud[0][0], width=cloud[0][1], height=cloud[0][2],
                                style={'maxWidth': 'auto', 'height': 'auto',
                                        'margin': '0 auto', 'display': 'block'}),
                    html.Details([
                                html.Summary('View Frequency Plot'),
                                dcc.Graph(id='word-freq', figure=cloud[1], config={'displayModeBar': False})
                    ])
                ])    
            ),
            html.Hr()
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

    def aggregate_by_time(self, data):
        # print(data["date"][0].utcoffset())
        data['hour'] = data.date.dt.hour
        data_grouped = data.groupby(data['hour']).size().reset_index(name ='count')
        data_grouped["h_percentage"] = data_grouped["count"]/len(data['hour']) *100
        data_grouped.index = data_grouped['hour']
        return data_grouped.reindex(np.arange(0, 23 + 1), fill_value=0)

    def filter_by_date_range_ads(self, start, stop):
        if start is not None and stop is not None:
            return (self.data[(self.data["date"] > start) \
                   & (stop > self.data["date"])])
        
        return self.data
    
    def filter_by_date_range(self, start, stop):
        if start is not None and stop is not None:
            return (self.data_cleaned[(self.data_cleaned["date"] > start) \
                   & (stop > self.data_cleaned["date"])])
        
        return self.data_cleaned
    #endregion

    #region DOM components
    def load_scatter(self, data):
        fig = px.scatter(x=data['date'],
                y=data['viewCount'],
                hover_name=data['title']
                )

        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Global Views", type='log')
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

        fig.update_layout(
            title=dict(x=0.5, text="Popularity of Watched Videos"), 
            xaxis_title="Date",
            yaxis_title="Views",
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="aliceblue"
        )
        return fig
    
    def load_time_trend_graph(self, data):
        
        fig = go.Figure()
        hour_data = self.aggregate_by_time(data)
        
        fig.add_trace(go.Scatter(y=hour_data['h_percentage'], x=hour_data.index, fill='tozeroy',
                            mode='none'
                            ))
    
        fig.update_layout(
            title=dict(x=0.5, text="Watched Video Hourly Trend"), 
            xaxis_title="Hour",
            yaxis_title="%",
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="aliceblue"
        )
        return fig
    
    def load_genre_graph(self, data):
        date_span = []
        fig = go.Figure()
        genre = defaultdict(list)
        grouped_data = data.groupby([pd.Grouper(key = 'date', freq='M')])
        categories = set(data['categoryName'])

        for r in grouped_data:
            if r[1].empty:
                continue

            date_span.append(r[0])
            category_span = set(r[1]['categoryName'])
            missing_groups = list(categories-category_span)
            tmpdf = r[1].groupby(['categoryName']).size().reset_index(name ='count')

            for c in missing_groups:
                tmpdf = pd.concat([tmpdf, pd.DataFrame.from_records([{"categoryName":c,"count":0}])])
            
            for i,r in tmpdf.iterrows():
                genre[r["categoryName"]].append(r["count"])

        for k,v in genre.items():
            # fig.add_trace(go.Scatter(x=date_span, y=v, fill='tozeroy',
            #                 mode='none',
            #                 name=k
            #                 ))

            fig.add_trace(go.Bar(x=date_span, y=v, name=k))

        fig.update_layout(
            barmode='group',
            title=dict(x=0.5, text="Genre Over Time"), 
            xaxis_title="Date",
            yaxis_title="Personal Views",
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="aliceblue"
        )
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
    
    def videos_rec(self, video_data):
        print (video_data)
        if len(video_data) > 0:
            return html.Div([
                html.H1('Recommended YouTube Videos'),
                html.Table([
                    html.Thead(html.Tr([
                        html.Th('Thumbnail'),
                        html.Th('Title'),
                        html.Th('Channel'),
                        html.Th('Views'),
                        html.Th('Likes'),
                        html.Th('Dislikes')
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td(html.Img(src=video['thumbnail'], height='90px')),
                            html.Td(html.A(video['title'], href=video['url'], target='_blank')),
                            html.Td(video['channel']),
                            html.Td(video['views']),
                            html.Td(video['likes']),
                        ]) for video in video_data
                    ])
                ])
            ])
        else:
            return html.Div([
                html.H1('No recommended videos found')
            ])
        

    def load_word_cloud(self, data):
        
        # Create the mask
        logo_mask = np.array(Image.open('./assets/youtube_logo.png'))
        # print(logo_mask)
        
        # Concatanate every entry in the table to one string        
        text = ""
        data = data.drop_duplicates()
        data = data.sort_values(by="viewCount", ascending=False)
        data = data[:200]
        for ind in data.index:
            text = text + " " + data['title'][ind]
        
        # Create word cloud!
        cloud = WordCloud(width=400, height=200, mask=logo_mask, background_color='black',
                      stopwords=STOPWORDS, max_words=50,
                      max_font_size=40, min_font_size=10,
                      random_state=19, scale=1, mode='RGB',
                      relative_scaling='auto', min_word_length=2, prefer_horizontal=0.4).generate(text)
        try:
            coloring = ImageColorGenerator(logo_mask)
            cloud.recolor(color_func=coloring)
        except:
            pass
        image = cloud.to_image()
    
        # Create bar chart
        byte_io = io.BytesIO()
        image.save(byte_io, 'PNG')
        byte_io.seek(0)
        data_uri = base64.b64encode(byte_io.getvalue()).decode('utf-8').replace('\n', '')
        src = 'data:image/png;base64,{0}'.format(data_uri)
        x = np.array(list(cloud.words_.keys()))
        y = np.array(list(cloud.words_.values()))
        order = np.argsort(y)[::-1]
        x = x[order]
        y = y[order]
        trace = go.Bar(x=x, y=y)
        layout = go.Layout(margin=go.layout.Margin(l=10, r=00),
                            title='Relative frequency of words')
        fig = go.Figure(data=[trace], layout=layout)
        
        # Create graphics to pass back
        # This version puts the cloud and freq charts next to each other
        # children = [
        #     dbc.Col(
        #         html.Img(id='word-cloud', src=src, width=image.size[0], height=image.size[1],
        #             style={'maxWidth': 'auto', 'height': 'auto',
        #                     'margin': '0 auto', 'display': 'block'})),
        #     dbc.Col(
        #         html.Details([
        #             html.Summary('View Frequency Plot'),
        #             dcc.Graph(id='word-freq', figure=fig, config={'displayModeBar': False})
        #         ])
        #     )
        # ]
        
        # This version puts the freq chart under the cloud
        # children = [
        #     dbc.Col([
        #         html.Img(id='word-cloud', src=src, width=image.size[0], height=image.size[1],
        #                     style={'maxWidth': 'auto', 'height': 'auto',
        #                             'margin': '0 auto', 'display': 'block'}),
        #         html.Details([
        #                     html.Summary('View Frequency Plot'),
        #                     dcc.Graph(id='word-freq', figure=fig, config={'displayModeBar': False})
        #         ])
        #     ])    
        # ]
        # return children
        
        # Output to make  the function only return the image and the figure
        # [[image source, width, height], bar chart]
        return [[src, image.size[0], image.size[1]], fig]

    #endregion
