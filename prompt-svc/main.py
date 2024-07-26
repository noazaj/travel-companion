# CS467 Online Capstone: GPT API Challenge
# Kongkom Hiranpradit, Connor Flattum, Nathan Swaim, Noah Zajicek

from flask import Flask, request, session
from flask_session import Session
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
# from flask import jsonify, send_file
# import requests
# import json
# import io

# from pytest import Session
from models import promptType, prompt

# Load ENV variables
load_dotenv(find_dotenv(".env"))

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=OPENAI_API_KEY)

# Set up Flask app
app = Flask(__name__)
HOST = os.getenv('PROMPT_SVC_HOST')
PORT = os.getenv('PROMPT_SVC_PORT')

# Load configurations from config.py file
# app.config.from_object('config.DevelopmentConfig')

# Configer Flask session variables
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

ERROR_MESSAGE_400 = {
    "svc": "prompt-svc",
    "Error": "The request body is invalid"
    }

# Message log for this session, stores all messages between GPT and user
# an array of 'message' objects
# 'message' objects is a dictionary of "role" and "content"
session_messages = []

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
@app.route('/v1/prompt/initial-req', methods=['POST'])
def initialRequest():

    content = request.get_json()

    print(content)
    # check that the request body is valid
    if ('destination' not in content or 'num-users' not in content or
            'num-days' not in content or 'preferences' not in content):
        return (ERROR_MESSAGE_400, 400)

    # extract variables from the request body content
    destination = content['destination']
    travelers_num = content['num-users']
    days_num = content['num-days']
    travel_preference = content['preferences']

    # create a session variable that stores all message logs
    # the message log is an array of 'message' objects
    # a 'message' objects is a dictionary of "role" and "content"
    session['messages'] = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "You are a professional vacation planner helping "
                        "users plan trips abroad. You will recommend hotels, "
                        "attractions, restaurants, shopping area, natural "
                        "sites or any other places that the user requests. "
                        "You will plan according to the budget and vacation "
                        "length given by the user. You will present the "
                        "result in a format of detailed itinerary of each "
                        "day, begin from day 1 to the last day."
                    )
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"Plan me a {days_num} days trip to {destination}. "
                        f"This is for a party of {travelers_num} adults aging "
                        f"from 35-38. We are interested in visiting shopping "
                        f"area, enjoying local food, with a one or two night "
                        f"life. We will strictly stay in Tokyo. Budget should "
                        f"be $1500 per person without airfare, but include "
                        f"ehotels, meals and other xpenses. We will be "
                        f"leaving from New York, USA. {travel_preference}"
                    )
                }
            ]
        }
    ]

    # call on GPT API with the message log
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=session['messages'],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

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

    session['messages'].append(new_message_object)

    print(completion.choices[0].message.content)

    return ({"gpt-message": completion.choices[0].message.content}, 200)

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
