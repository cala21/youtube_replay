
from dash.dependencies import Input, Output, State
from utils import Utils
from YouTubeOAuthClient import YouTubeOAuthClient
from dash import html
from config.definitions import ROOT_DIR
import os
import flask

def get_callbacks(app):
    utils = Utils()
    # Create an instance of the YouTubeOAuthClient class
    # Define the scopes and client secrets file
    print(os.path.join(ROOT_DIR, 'assets', 'client_secret.json'))

    # This variable specifies the name of a file that contains the OAuth 2.0
    # information for this application, including its client_id and client_secret.
    client_secrets_file = os.path.join(ROOT_DIR, 'assets', 'client_secret.json')
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    youtube = YouTubeOAuthClient(scopes, client_secrets_file)

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
    
    @app.callback(
    [Output('word-cloud', 'src'),
     Output('word-cloud', 'width'),
     Output('word-cloud', 'height'),
     Output('word-freq', 'figure')],
    [Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')])
    def update_word_cloud(start_date, end_date):
        data = utils.filter_by_date_range(start_date, end_date)
        output = utils.load_word_cloud(data)
        print(output)
        src, width, height, figure = output[0][0], output[0][1], output[0][2], output[1]
        return src, width, height, figure
            

    # Define a callback function to handle the button click event
    @app.callback(
        Output("youtube-data", "children"),
        [Input("btn-google", "n_clicks")],
        )
    def connect_with_google(n_clicks):
        if 'credentials' not in flask.session:
            print("Credentials not in session.")
            auth_url = youtube.get_auth_url()
            return html.A('Connect with YouTube Account', href=auth_url)
        else:
                youtube.fetch_creds()
                data = youtube.get_channel_data(
                    part="snippet,statistics",
                    mine=True,
                )
                # Return the data as a Dash component
                return html.Div([
                    html.H1(data["items"][0]["snippet"]["title"]),
                    html.Img(src=data["items"][0]["snippet"]["thumbnails"]["medium"]["url"]),
                    html.P(f"Subscribers: {data['items'][0]['statistics']['subscriberCount']}"),
                    html.P(f"Total views: {data['items'][0]['statistics']['viewCount']}"),
                    html.P(f"Total videos: {data['items'][0]['statistics']['videoCount']}"),
                    ])

        
    # Define a callback function to handle the button click event
    @app.callback(
        Output("btn-google", "n_clicks"),
        [Input("btn-creds", "n_clicks")],
        )
    def clear_credentials(n_clicks):
        if n_clicks:
            youtube.clear_credentials()
            print("Credentials cleared.")
            return 0
