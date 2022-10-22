import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request, url_for, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "q43w56erutjkgmfds35465t"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://BooksRiver.elsie094081.repl.co/callback"
)

def google_login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect(url_for('login'))
        else:
            return function()

    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/home')
@google_login_required
def home():
    return render_template('home.html', username=session['name'])


if __name__ == '__main__':
    app.run(port=8040, host='0.0.0.0', debug=False)
