import base64
from datetime import datetime
import re
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
from scipy.ndimage import gaussian_gradient_magnitude
import warnings; warnings.filterwarnings("ignore")
from config.definitions import ROOT_DIR
import os
import pandas as pd

# Added for word cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

class Utils:

    TZ_DICT = {'US/Mountain':'MST', 'US/Pacific':'PST', 'US/Central':'CST', 'US/Eastern':'EST'}
    AGGR_DICT = {'Y':'Yearly','Q':'Quarterly','SM':'Semi-Monthly','M':'Monthly', 'W':'Weekly'}

    def __init__(self):
        self.data = []
        self.data_rec = []
        self.cloud_words = {}
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
            "snippet.tags": "tags",
            "statistics.viewCount": "viewCount",
            "statistics.likeCount": "likeCount",
            "statistics.commentCount": "commentCount"})
        data_norm = data_norm.merge(watched_videos[["id","date"]], how="left", on="id")
        data_norm['categoryName'] = data_norm.apply(lambda x: categories[x['categoryId']]["categoryName"], axis=1)
        data_norm.sort_index(inplace=True)

        return data_norm[["id","date","categoryName","tags","title","description","duration","categoryId","viewCount","likeCount","commentCount"]]
    
    def clean_categories(self, location="US"):
        category_details = self.yth.get_video_category(location)
        data_norm = pd.json_normalize(category_details["items"])
        data_norm = data_norm.rename(columns={"snippet.title": "categoryName"})

        return data_norm[["id","categoryName"]].set_index("id").to_dict('index')
    
    def top_watch(self, data):
        data['count'] = 1
        dfcount = data.groupby(["title","categoryName","viewCount","likeCount"], as_index = False)['count'].sum().sort_values(by =['count'],ascending=False).head(5)
        self.data_rec = (dfcount.merge(data[["title","tags"]], how="left", on="title")).drop_duplicates(['title'])
        
        del dfcount['count']
        dfcount['viewCount'] = dfcount['viewCount'].apply(lambda x: "{:,}".format(int(x)))
        dfcount['likeCount'] = dfcount['likeCount'].apply(lambda x: "{:,}".format(int(x)))
        dfcount = dfcount.rename(columns={'title':'Title', 'categoryName':'Category','viewCount':'Overall Views','likeCount':'Overall Likes'})
        dfdic = dfcount.to_dict('records')
        dfcol = [{"name": i, "id": i} for i in (dfcount.columns)]
        return dfdic, dfcol

    def get_video_rec(self):
        x = np.array(list(self.cloud_words.keys()))
        y = np.array(list(self.cloud_words.values()))
        order = np.argsort(y)[::-1]
        x = x[order]

        key_words = list(self.data_rec["tags"].explode())
        res_t = [str(idx) for idx in key_words if not re.findall("[^\u0000-\u05C0\u2100-\u214F]+", str(idx))]
        res_x = [str(idx) for idx in x if not re.findall("[^\u0000-\u05C0\u2100-\u214F]+", str(idx))]
        merged_words = res_x + res_t
        param_merged_words = "|".join(merged_words)
        search_response = self.yth.search(param_merged_words,len(param_merged_words))
        video_ids = pd.json_normalize(search_response["items"])["id.videoId"]
        v_ids_s = ",".join(video_ids)
        video_data_details = self.yth.get_video_details(v_ids_s)
        df = pd.json_normalize(video_data_details["items"])
        df = df.rename(columns={"snippet.title": "title",
            "snippet.thumbnails.default.url": "thumbnail",
            "statistics.viewCount": "viewCount",
            "statistics.likeCount": "likeCount",
            "snippet.channelTitle": "channelTitle"})
        df = df[["title","thumbnail","viewCount","likeCount","channelTitle"]].dropna(subset=['viewCount'])
        df['viewCount'] = df['viewCount'].astype('int')
        df = df.sort_values(by="viewCount", ascending=False)
        return df[:5]

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
                        dbc.Col(
                            dcc.Graph(
                                id='views-scatter',
                                figure=self.load_scatter(self.data_cleaned)
                            ),style = {'marginLeft':'1px', 'marginTop':'7px', 'marginRight':'1px'}
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="ads-graph",
                                figure=self.load_graph(self.data)
                            ),style = {'marginLeft':'1px', 'marginTop':'7px', 'marginRight':'1px'}
                        )
                    ]
                ),

                dbc.Row(
                    children=[
                        dbc.Col(
                            html.Div(children=[
                                dcc.Dropdown(self.AGGR_DICT, placeholder='Yearly', id='g-dropdown'),
                                dcc.Graph(
                                id='genre-graph',
                                figure=self.load_genre_graph(self.data_cleaned)
                                )
                        ]),style = {'marginLeft':'1px', 'marginTop':'7px', 'marginRight':'1px'}),
                        dbc.Col(
                            html.Div(children=[
                                dcc.Dropdown(self.TZ_DICT, placeholder='PST', id='tz-dropdown'),
                                dcc.Graph(
                                    id='time-graph',
                                    figure=self.load_time_trend_graph(self.data_cleaned)
                                )
                            ])
                            ,style = {'marginLeft':'1px', 'marginTop':'7px', 'marginRight':'1px'})
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col([
                            html.Label("My Most Watched Videos", style={'font-family':'sans-serif',
                                                                        'fontWeight': 'bold',
                                                                        'font-size': '1.em',
                                                                        'color': '#d9230f'}),
                            dash_table.DataTable(
                                data = self.top_watch(self.data_cleaned)[0],
                                columns = self.top_watch(self.data_cleaned)[1],
                                id = 'top-watch',
                                style_table = {'overflowX': 'auto'},
                                style_cell={'font-family':'sans-serif'},
                                style_as_list_view=True,
                                style_header={
                                    'backgroundColor': '#f8f8f8',
                                    'fontWeight': 'bold',
                                    'textAlign': 'left'
                                },
                                style_data={
                                    'color': 'black',
                                    'height': 'auto',
                                    'backgroundColor': '#fcfcfc',
                                    'textAlign': 'left'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': '#f8f8f8',
                                        'height': 'auto',
                                        'textAlign': 'left'
                                    }
                                ],
                            ),
                        ],style = {'marginLeft':'1px', 'marginTop':'7px', 'marginRight':'1px'})   
                    ] 
                ),
                html.Hr(),
                dbc.Button(
                    "Toggle Word Cloud",
                    id="toggle-word-cloud-button",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Row(
                        children=[
                            dbc.Col([
                                html.Img(id='word-cloud', src=cloud[0][0], width=cloud[0][1], height=cloud[0][2],
                                            style={'maxWidth': 'auto', 'height': 'auto',
                                                    'margin': '0 auto', 'display': 'block'})
                            ],style = {'marginLeft':'1px', 'marginTop':'7px', 'marginRight':'1px'}),
                        ]
                    ),
                    id="toggle-word-cloud",
                    is_open=False,
                    dimension="width"
                ),
                html.Hr(),
                dbc.Button(
                    "Toggle History Based Recommendation",
                    id="toggle-hist-rec-button",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Row(
                        children=[
                            dbc.Col([
                                html.Div(id='container-rec',
                                    children=[dbc.Table.from_dataframe(self.load_recommendation(),
                                                            striped=True, 
                                                            bordered=True,
                                                            hover=True,
                                                            style={'font-family':'sans-serif'})
                                ])
                            ])   
                        ] 
                    ),
                    id="toggle-hist-rec",
                    is_open=False,
                    dimension="width"
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

    def aggregate_by_time(self, data, timezone):
        data.index = pd.to_datetime(data['date'], utc=True)
        data.index = data.index.tz_convert(timezone)
        data['hour'] = data.index.hour
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
    
    def load_time_trend_graph(self, data, tz='US/Pacific'):
        
        fig = go.Figure()
        hour_data = self.aggregate_by_time(data, tz)
        
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
    
    def load_genre_graph(self, data, freq='Y'):
        date_span = []
        fig = go.Figure()
        genre = defaultdict(list)
        grouped_data = data.groupby([pd.Grouper(key = 'date', freq=freq)])
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
        
    def load_recommendation(self):
        data = self.get_video_rec()
        data['thumbnail'] = data['thumbnail'].apply(lambda x: html.Img(src=x, height='90px'))
        data['viewCount'] = data['viewCount'].apply(lambda x: "{:,}".format(int(x)))
        data['likeCount'] = data['likeCount'].apply(lambda x: "{:,}".format(int(x)))
        data = data.rename(columns={'title':'Title', 'thumbnail':'Thumbnail','viewCount':'Overall Views','likeCount':'Overall Likes','channelTitle':'Channel'})
        return data
    
    def load_word_cloud(self, data):
        # Create the mask
        youtube_logo = os.path.join(ROOT_DIR, 'assets', 'youtube_logo.png')

        logo = np.array(Image.open(youtube_logo))

        # create mask  white is "masked out"
        logo_mask = logo.copy()
        logo_mask[logo_mask.sum(axis=2) == 0] = 255
        edges = np.mean([gaussian_gradient_magnitude(logo[:, :, i] / 255., 2) for i in range(3)], axis=0)
        logo_mask[edges > .08] = 255
        
        # Concatenate every entry in the table to one string        
        text = ""
        data = data.drop_duplicates(['title']).dropna(subset=['viewCount'])
        data['viewCount'] = data['viewCount'].astype('int')
        data = data.sort_values(by="viewCount", ascending=False)

        # Grab top 20%
        l_data = len(data)
        if l_data > 1:
            top = int(l_data*0.2)
            data = data[:top]

        for ind in data.index:
            text = text + " " + data['title'][ind].lower() + '.'

        # Create word cloud!
        stopwords = set(STOPWORDS)
        stopwords.update(['short', 'shorts', 'ft', 'official','let','feat'])

        cloud = WordCloud(width=400, height=200, mask=logo_mask, background_color='#fcfcfc',
                    stopwords=stopwords, max_words=l_data,
                    random_state=42,max_font_size=40, min_word_length=3,
                    scale=0.7,relative_scaling='auto', prefer_horizontal=0.4).generate(text)
        self.cloud_words = cloud.words_

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

        return (src, image.size[0], image.size[1])

    #endregion
