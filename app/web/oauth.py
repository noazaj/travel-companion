from flask import Blueprint, url_for, session, redirect, current_app, abort, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import json, secrets

load_dotenv()

oauth_bp = Blueprint('oauth', __name__)
oauth = OAuth()

def configure_oauth(app):
    oauth.init_app(app=app)
    providers = app.config['OAUTH2_PROVIDERS']
    
    for provider, config in providers.items():
        oauth.register(
            name=provider,
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            access_token_url=config['token_url'],
            access_token_params=None,
            authorize_url=config['authorize_url'],
            authorize_params=None,
            api_base_url=config['userinfo']['url'],
            client_kwargs={'scope': ' '.join(config['scopes'])}
        )


@oauth_bp.route('/login/<provider>')
def oauth2_login(provider):
    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)
        
    # Generate random string for state parameter
    state = secrets.token_urlsafe(16)
    session['oauth2_state'] = state
    
    # Dynamically create the client and authorize redirect
    redirect_uri = url_for('oauth.oauth2_authorize', provider=provider, _external=True)
    return oauth.create_client(provider).authorize_redirect(redirect_uri, state=state)


##############################################
#
# Create the redirect authorization endpoint to show user profile
# Retrieve the token, profile, and store it in the session
#
##############################################
@oauth_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    # Create the client to be used for authorization
    client = oauth.create_client(provider)
    if not client:
        abort(404)
    
    try:
        # Validate state parameter
        if request.args.get('state') != session.get('oauth2_state'):
            abort(403)
        
        token = client.authorize_access_token()
        session['token'] = token
        resp = client.get('user', token=token)
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
