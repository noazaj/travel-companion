# CS467 Online Capstone: GPT API Challenge
# Kongkom Hiranpradit, Connor Flattum, Nathan Swaim, Noah Zajicek

from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import os
from models import promptType, prompt

# Load ENV variables
load_dotenv(find_dotenv(".env"))

# Set up Flask app
app = Flask(__name__)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


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
@app.route('/v1/prompt/chat', methods=['GET', 'POST'])
def chatPrompt():

    history = request.args.get('history')
    text = request.args.get('text')

    if text is None:
        text = (
            "Plan me a 7 days trip to Tokyo, Japan. This is for a party of "
            "4 adults aging from 35-38. We are interested in visiting "
            "shopping area, enjoying local food, with a one or two night "
            "life. We will strictly stay in Tokyo. Budget should be $1500 "
            "per person without airfare, but include hotels, meals and other "
            "expenses. We will be leaving from New York, USA."
          )

    answer = None

    options = {
        history: history,
        text: text,
    }

    try:
        p = prompt.Prompt()
        answer = p.prompt(promptType.PromptType.ChatCompletions,
                          options)
    except TypeError:
        return {
            "svc": "prompt-svc",
            "msg": "Invalid type: please use 1) chat,\
                2) embedded, or 3) image",
            "text": text,
            "history": history,
        }

    return {
        "history": history,
        "text": text,
        "answer": answer,
    }


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)

# Resources used:
#   - https://medium.com/@abed63/flask-application-with-openai-
#     chatgpt-integration-tutorial-958588ac6bdf
#   - https://medium.com/@jcrsch/openai-assistant-with-flask-
#     a-simple-example-with-code-d007ac42ced2
#
