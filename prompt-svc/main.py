# CS467 Online Capstone: GPT API Challenge
# Kongkom Hiranpradit, Connor Flattum, Nathan Swaim, Noah Zajicek

from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import os

# from pytest import Session
from models import promptType, prompt

# Load ENV variables
load_dotenv(find_dotenv(".env"))

# Set up Flask app
app = Flask(__name__)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# Load configurations from config.py file
# app.config.from_object('config.DevelopmentConfig')

# Configer Flask session variables
app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

ERROR_MESSAGE_400 = {
    "svc": "prompt-svc",
    "Error": "The request body is invalid"
    }


###########################################################
#
#  Endpoint to check if prompt-svc is running
#
###########################################################
@app.route('/')
def index():
    return {
        "svc": "prompt-svc",
        "msg": "prompt service is up and running!"
    }


###########################################################
#
#  Route to use prompts with chatGPT API
#
#  Receives:
#   - history:  a history of the conversation
#   - text:     the text of the question to ask
#
#  Returns:
#   - history:  a history of the conversation
#   - text:     the text of the question to ask
#   - answer:   answer to the question prompted
#
###########################################################
@app.route('/v1/prompt/itinerary', methods=['POST'])
def chatPrompt():

    print(request.get_data())

    # get json body from POST request
    content = request.get_json()

    # check that the request body is valid
    if ('messages' not in content):
        return (ERROR_MESSAGE_400, 400)

    try:
        p = prompt.Prompt()
        completion = p.prompt(promptType.PromptType.ChatCompletions,
                              content['messages'])

    except TypeError:
        return {
            "svc": "prompt-svc",
            "msg": "Invalid type: please use 1) chat,\
                2) embedded, or 3) image",
            "messages": content['messages'],
        }

    # check that the request body is valid
    if ('error' in completion):
        return {
            "svc": "prompt-svc",
            "error": completion['error'],
            "messages": content['messages'],
        }

    # manually add GPT's reply message to message log
    new_message_object = {
            "role": completion.choices[0].message.role,
            "content": [
                {
                    "type": "text",
                    "text": completion.choices[0].message.content
                }
            ]
        }
    content['messages'].append(new_message_object)

    return {
        "svc": "prompt-svc",
        "messages": content['messages'],
    }


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)

# Resources used:
#   - https://medium.com/@abed63/flask-application-with-openai-
#     chatgpt-integration-tutorial-958588ac6bdf
#   - https://medium.com/@jcrsch/openai-assistant-with-flask-
#     a-simple-example-with-code-d007ac42ced2
#
