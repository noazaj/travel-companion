from flask import Blueprint, url_for
from authlib.integrations.flask_client import OAuth
import os

oauth_bp = Blueprint('oauth', __name__)
oauth = OAuth()

# Setup oauth register for Github with designated parameters
oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


# Create the login endpoint for github
@oauth_bp.route('/login/github')
def github_login():
    redirect_uri = url_for('oauth.github_authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


# Create the redirect authorization endpoint to show user profile
@oauth_bp.route('/auth/github')
def github_authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user', token=token)
    profile = resp.json()
    return f'User profile: {profile}'


# Resources Used:
# https://docs.authlib.org/en/latest/client/frameworks.html#frameworks-clients
# https://flask.palletsprojects.com/en/3.0.x/blueprints/