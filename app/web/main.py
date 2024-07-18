from flask import Flask
from oauth import oauth_bp, oauth
from web import web_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialize OAuth and register blueprints
oauth.init_app(app)
app.register_blueprint(oauth_bp)
app.register_blueprint(web_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True,
            host=os.getenv('FLASK_RUN_HOST'),
            port=os.getenv('FLASK_RUN_PORT'))
