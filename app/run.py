import index
import YouTubeOAuthFlaskServer
import os

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

    index.app.run_server(host='0.0.0.0', port=8080, threaded=True, debug=True)
