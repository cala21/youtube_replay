
import time
from dash.dependencies import Input, Output, State
from utils import Utils
from YouTubeOAuth import YouTubeOAuth
from dash import html
from config.definitions import ROOT_DIR
import os

def get_callbacks(app):
    utils = Utils()
    # Create an instance of the YouTubeOAuth class
    # Define the scopes and client secrets file
    print(os.path.join(ROOT_DIR, 'assets', 'client_secret.json'))

    # This variable specifies the name of a file that contains the OAuth 2.0
    # information for this application, including its client_id and client_secret.
    client_secrets_file = os.path.join(ROOT_DIR, 'assets', 'client_secret.json')
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    youtube = YouTubeOAuth(scopes, client_secrets_file)

    @app.callback(Output('output-data-upload', 'children'),
                Input('upload-data', 'contents'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                utils.parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]

            return children

    @app.callback(
    Output('history-table', 'data'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_output(start_date, end_date):
        start_date_string, end_date_string =  utils.parse_date(start_date, end_date)

        return utils.filter_by_date_range(start_date_string, end_date_string)[["date","title"]].to_dict('records')
    
    @app.callback(
    Output('ads-graph', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_graph(start_date, end_date):
        data = utils.filter_by_date_range_ads(start_date, end_date)

        return utils.load_graph(data)
    
    @app.callback(
    Output('views-scatter', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_scatter(start_date, end_date):
        data = utils.filter_by_date_range(start_date, end_date)

        return utils.load_scatter(data)
    
    @app.callback(
    Output('genre-graph', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_genre_graph(start_date, end_date):
        data = utils.filter_by_date_range(start_date, end_date)

        return utils.load_genre_graph(data)
    
    @app.callback(
    Output('time-graph', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_genre_graph(start_date, end_date):
        data = utils.filter_by_date_range(start_date, end_date)

        return utils.load_time_trend_graph(data)
    
    # Define a callback function to handle the button click event
    @app.callback(
        Output("youtube-data", "children"),
        [Input("btn-google", "n_clicks")],
        )
    def connect_with_google(n_clicks):
        if n_clicks:
            youtube.authenticate()
            data = youtube.fetch_data(
                part="snippet",
                fields="items(id(videoId),snippet(title))",
                q="surfing",
                type="video",
                maxResults=10,
            )
            # Format the data as a string
            youtube_data_str = " ".join([f"{k}: {v}" for k, v in data.items()])
        
            # Return the data as a Dash component
            return html.Div(youtube_data_str)
        else :
            return ""