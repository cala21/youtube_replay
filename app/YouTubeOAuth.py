import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import flask

class YouTubeOAuth:
    def __init__(self, scopes, client_secrets_file):
        self.scopes = scopes
        self.client_secrets_file = client_secrets_file
        self.credentials = None
   
    def authenticate(self):
        """Authenticates the user and stores the credentials."""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, scopes=self.scopes
        )
        self.credentials = flow.run_local_server(port=8081)

    def fetch_data(self, part, fields, **kwargs):
        """Fetches data from the YouTube API."""
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.authenticate()

        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=self.credentials)
        kwargs["part"] = part
        kwargs["fields"] = fields
        try:
            #response = youtube.search().list(**kwargs).execute()
            response = youtube.channels().list(part='snippet,statistics', mine=True).execute()
            print(response)
            return response
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


    # def get_authorization_url(self):
    #     # This variable specifies the name of a file that contains the OAuth 2.0
    #     # information for this application, including its client_id and client_secret.
    #     CLIENT_SECRETS_FILE = os.path.join(ROOT_DIR, 'assets', 'client_secret.json')

    #     # This OAuth 2.0 access scope allows for full read/write access to the
    #     # authenticated user's account and requires requests to use an SSL connection.
    #     SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
        
    #     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    #     flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    #     auth_url, state = flow.authorization_url(
    #         access_type='offline',
    #         include_granted_scopes='true'
    #     )
    #     return auth_url


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
