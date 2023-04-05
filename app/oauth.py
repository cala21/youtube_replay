import index
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import os
from config.definitions import ROOT_DIR

print(os.path.join(ROOT_DIR, 'assets', 'client_secret.json'))

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = os.path.join(ROOT_DIR, 'assets', 'client_secret.json')

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

#App Secret
server = index.app.server
server.config.update(
    SECRET_KEY=os.urandom(12),
)

@server.route('/test')
def test_api_request():
  if 'credentials' not in flask.session:
    print("Creds not in Session")
    return flask.redirect('authorize')
  
  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  youtube = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)
  video_id = 'dQw4w9WgXcQ'

  vidoes = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
  #channels = youtube.channels().list(part='snippet,statistics', id=video_id).execute()

  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.jsonify(**vidoes)


@server.route('/authorize')
def authorize():
  print("In Authorization")

  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  print(state)
  flask.session['state'] = state

  return flask.redirect(authorization_url)


@server.route('/oauth2callback')
def oauth2callback():
  print("In Oauth Callback")

  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  print(credentials)

  flask.session['credentials'] = credentials_to_dict(credentials)
  print(flask.session['credentials'] )
  return flask.redirect(flask.url_for('test_api_request'))


@server.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' )
  else:
    return('An error occurred.' )


@server.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    print("Deleting Credentials")
    print(flask.session['credentials'] )
    del flask.session['credentials']

    return ('Credentials have been cleared.<br><br>')

  else:
    print("Cannot Delete Credentials")
    return ('Credentials are not present and cannot be cleared.<br><br>')

@server.route('/logout')
def logout():
  logout_url ='https://accounts.google.com/Logout'
  if 'credentials' in flask.session:
    print("Deleting Credentials")
    del flask.session['credentials']
  return flask.redirect(logout_url)

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}
