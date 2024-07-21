import os
from dotenv import load_dotenv

# Load enviornment varaibles from .env file
load_dotenv()


class Config:
    """ Setup config settings for authorization. This class
    instantiation will grow in the future. """
    SECRET_KEY = os.getenv('SECRET_KEY')
    OAUTH2_PROVIDERS = {
        # Github OAuth 2.0 documentation:
        # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
        'github': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'token_url': 'https://github.com/login/oauth/access_token',
            'api_base_url': 'https://api.github.com/',
            'client_kwargs': {'scope': 'user:email'},
        },

        # Google OAuth 2.0 documentation:
        # https://developers.google.com/identity/protocols/oauth2
        'google': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'token_url': 'https://accounts.google.com/o/oauth2/token',
            'api_base_url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'client_kwargs': {'scope': 'openid profile email'},
            'jwks_uri': 'https://www.googleapis.com/oauth2/v3/certs',
        },

        # Facebook OAuth 2.0 documentation:
        # https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow/
        'facebook': {
            'client_id': os.getenv('FACEBOOK_CLIENT_ID'),
            'client_secret': os.getenv('FACEBOOK_CLIENT_SECRET'),
            'authorize_url': 'https://www.facebook.com/v20.0/dialog/oauth?',
            'token_url': (
                'https://graph.facebook.com/v20.0/'
                'oauth/access_token?'
            ),
            'api_base_url': 'https://graph.facebook.com/',
            'client_kwargs': {'scope': 'email'}
        },
    }


# Create a development config class for testing purposes
class DevelopmentConfig(Config):
    DEBUG = True


# Create a production config class when getting ready to push for production
class ProductionConfig(Config):
    DEBUG = False
