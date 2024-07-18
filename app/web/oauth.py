from flask import Blueprint, url_for, session, redirect
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import json

load_dotenv()

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


########################################
#
# Create the login endpoint for github
#
########################################
@oauth_bp.route('/login/github')
def github_login():
    redirect_uri = url_for('oauth.github_authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


##############################################
#
# Create the redirect authorization endpoint to show user profile
# Retrieve the token, profile, and store it in the session
#
##############################################
@oauth_bp.route('/auth/github')
def github_authorize():
    try:
        token = oauth.github.authorize_access_token()
        session['token'] = token
        resp = oauth.github.get('user', token=token)
        profile = resp.json()
        session['profile'] = profile
        return redirect(url_for('oauth.profile'))
    except Exception as err:
        return f'Authorization failed: {err}', 400


########################################
#
# Create a profile endpoint to display user profile
#
########################################
@oauth_bp.route('/profile')
def profile():
    profile = session.get('profile')
    if not profile:
        return redirect(url_for('oauth.github_login'))
    json_profile = json.dumps(profile, indent=4)
    return (
        f"Hello, {profile['name']}!\n\n"
        "Here is your current information:\n\n"
        f"{json_profile}"
    )

# Resources Used:
# https://docs.authlib.org/en/latest/client/frameworks.html#frameworks-clients
# https://flask.palletsprojects.com/en/3.0.x/blueprints/
