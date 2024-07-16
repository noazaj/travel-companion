from flask import Flask
from app.web.oauth import oauth, oauth_bp

# Create Flask application
app = Flask(__name__)

# Load configurations from config.py file
app.config.from_object('config.DevelopmentConfig')

# Initialize OAuth with the created Flask app
oauth.init_app(app)

# Register OAuth blueprint
app.register_blueprint(oauth_bp)


@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the home page!'


if __name__ == '__main__':
    app.run()
