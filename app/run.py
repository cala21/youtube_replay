import index
from flask import Flask, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SECRET_KEY'] = os.urandom(12)

oauth = OAuth(app)
#index.app.secret_key = os.urandom(12)
#oauth = OAuth(index.app)
server = index.app.server


@server.route('/google/')
def google():

    GOOGLE_CLIENT_ID = '782606518020-5taujji8ts1k0hgcda4q01tum1phj95h.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@server.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    return redirect('/')

if __name__ == '__main__':
    index.app.run_server(host='0.0.0.0', port=8080, debug=True)
