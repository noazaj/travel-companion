from flask import Flask
from oauth import oauth_bp, configure_oauth
from web import web_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    
    # Initialize OAuth2.0 providers configurations
    configure_oauth(app)
    
    # Initialize OAuth and register blueprints
    app.register_blueprint(oauth_bp)
    app.register_blueprint(web_bp, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,
            host=os.getenv('FLASK_RUN_HOST'),
            port=os.getenv('FLASK_RUN_PORT'))
