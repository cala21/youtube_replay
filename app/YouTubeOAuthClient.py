from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import flask

#YouTubeOauthClient
class YouTubeOAuthClient:
    def __init__(self, scopes, client_secrets_file):
        self.scopes = scopes
        self.client_secrets_file = client_secrets_file
        self.credentials = None
   
    def get_auth_url(self):
        flow = Flow.from_client_secrets_file(
            self.client_secrets_file, scopes=self.scopes
        )
        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
        print("Saving state in session.")
        flask.session['state'] = state
        return authorization_url
    
    def fetch_creds(self):
        self.credentials = Credentials(
        **flask.session['credentials'])

    def fetch_token(self, authorization_response):
        flow = Flow.from_client_secrets_file(
            self.client_secrets_file, self.scopes)
        flow.fetch_token(authorization_response=authorization_response)
        self.credentials = flow.credentials

    def get_channel_data(self, part, mine, **kwargs):
        """Fetches data from the YouTube API."""
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.authenticate()

        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=self.credentials)
        kwargs["part"] = part
        kwargs["mine"] = mine
        try:
            response = youtube.channels().list(**kwargs).execute()
            return response
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        
    def get_rec_data(self):
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.authenticate()
        try:
            youtube = googleapiclient.discovery.build("youtube", "v3", credentials=self.credentials)
            videos_response = youtube.videos().list(myRating='like', part='snippet').execute()
            video_ids = [item['id'] for item in videos_response['items']]
            print("video_ids")

            print(video_ids)

            recommendations = []
            video_data = []
            for video_id in video_ids:
                recommendations_response = youtube.search().list(relatedToVideoId=video_id, type='video', part='snippet').execute()
                recommendations.extend([item['id']['videoId'] for item in recommendations_response['items']])
            print(recommendations)
            for video_id in recommendations:
                video_response = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
                print(video_response['items'][0]['statistics'])
                print(video_response['items'][0]['snippet'])

                video_title = video_response['items'][0]['snippet']['title']
                video_channel = video_response['items'][0]['snippet']['channelTitle']
                video_views = video_response['items'][0]['statistics'].get('viewCount', 0)
                video_likes = video_response['items'][0]['statistics'].get('likeCount', 0)
                video_thumbnail = video_response['items'][0]['snippet']['thumbnails']['default']['url']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_data.append({'title': video_title, 'channel': video_channel, 'views': video_views, 'likes': video_likes, 'thumbnail': video_thumbnail, 'url': video_url})

            return video_data

                #print(f'Title: {video_title}\nChannel: {video_channel}\nViews: {video_views}\nLikes: {video_likes}\n, Thumbnail: {video_thumbnail}, url {video_url}')
                    
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        

        
    def revoke_credentials(self):
        if self.credentials:
            http = self.credentials.authorize(Request())
            try:
                Credentials.from_authorized_user_info(info=None)
                http = self.credentials.authorize(Request())
                response = http.request(
                    "GET",
                    "https://oauth2.googleapis.com/revoke?token=" + self.credentials.token,
                    headers={"content-type": "application/x-www-form-urlencoded"},
                )
                self.credentials = None
                print("Credentials successfully revoked.")
            except:
                print("Error revoking credentials.")    
        else:
                print("No credentials to revoke.")    
    
    def clear_credentials(self):
        if 'credentials' in flask.session:
            del flask.session['credentials']
            self.credentials = None


    


    # def set_credentials(self, authorization_response):
       
    #     CLIENT_SECRETS_FILE = os.path.join(ROOT_DIR, 'assets', 'client_secret.json')
    #     SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
        
    #     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    #     flow.fetch_token(authorization_response=authorization_response)
    #     self.credentials = flow.credentials

    # def get_youtube_data(self):
    #     youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=self.credentials)
    #     channels_response = youtube.channels().list(
    #         mine=True,
    #         part='snippet,contentDetails,statistics'
    #     ).execute()
    #     channels = channels_response.get('items', [])
    #     if not channels:
    #         return None
    #     else:
    #         return channels[0]['snippet']['title'], channels[0]['statistics']
