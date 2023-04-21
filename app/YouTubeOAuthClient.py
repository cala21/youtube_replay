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
        print("adding state")
        flask.session['state'] = state
        print(authorization_url)
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
