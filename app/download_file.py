from flask import send_file
import os
from config.definitions import ROOT_DIR
import index
server = index.app.server
server.config.update(
    SECRET_KEY=os.urandom(12),
)
@server.route('/assets/watch_history.json')
def download_watch_history():
    filename = 'watch_history.json'
    filepath = os.path.join(ROOT_DIR, 'assets', filename)
    return send_file(filepath, as_attachment=True, attachment_filename=filename)
