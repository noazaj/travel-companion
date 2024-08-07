from flask import Flask, g
from app.auth.oauth import oauth_bp, configure_oauth
from app.routes.web import web_bp, fetch_weather_update
from db.connection import connect_pg
from dotenv import load_dotenv
import threading

load_dotenv()

notification_update = {}


def start_notification_thread():
    notification_thread = threading.Thread(target=fetch_weather_update)
    notification_thread.start()


app = Flask(__name__)
app.config.from_object('app.config.DevelopmentConfig')


# Store the connection in g
@app.before_request
def before_request():
    if 'conn' not in g:
        g.conn = connect_pg()

@app.teardown_appcontext
def teardown_appcontext(exception):
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()

# Initialize OAuth2.0 providers configurations
configure_oauth(app)

# Initialize OAuth and register blueprints
app.register_blueprint(oauth_bp)
app.register_blueprint(web_bp, url_prefix='/')

# Start the notification thread
start_notification_thread()


if __name__ == '__main__':
    app.run()
