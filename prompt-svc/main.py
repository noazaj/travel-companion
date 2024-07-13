from flask import Flask
import prompt
# import json


app = Flask(__name__)

HOST = 'http://localhost'
PORT = 8080


@app.route('/')
def index():
    return {
        "svc": "prompt-svc",
        "msg": "prompt service is up and running!"
    }


@app.route('/prompt/<type>/<options>')
def chatPrompt(type, options):

    try:
        return prompt.prompt(type, options).to_json()
    except TypeError:
        return {
            "svc": "prompt-svc",
            "msg": "Invalid type: please use 1) chat, 2) embedded, or 3) image"
        }


if __name__ == "__main__":
    app.run()
