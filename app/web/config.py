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
            'userinfo': {
                'url': 'https://api.github.com/user/emails',
                'email': lambda json: json[0]['emails'],
            },
            'scopes': ['user:email'],
        },
    }


# Create a development config class for testing purposes
class DevelopmentConfig(Config):
    DEBUG = True


# Create a production config class when getting ready to push for production
class ProductionConfig(Config):
    DEBUG = False
