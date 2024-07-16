import os
from dotenv import load_dotenv

# Load enviornment varaibles from .env file
load_dotenv()

class Config:
    """ Setup config settings for authorization. This class instantiation will grow 
     in the future. """
    SECRET_KEY = os.getenv('SECRET_KEY')
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')


# Create a development config class for testing purposes
class DevelopmentConfig(Config):
    DEBUG = True

# Create a production config class when getting ready to push for production
class ProductionConfig(Config):
    DEBUG = False