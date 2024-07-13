from flask import Flask, request
from models import promptType, prompt, assistant
# import json


app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 8080


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
    answer = None

    try:
        answer = prompt.prompt(promptType.PromptType.ChatCompletions,
                               prompt).to_json()
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
@app.route('/v1/prompt/assistant', methods=['GET', 'POST'])
def assistantPrompt():

    history = request.args.get('history')
    text = request.args.get('text')
    answer = None

    try:
        # TODO: implement assistant module endpoint
        answer = assistant.Assistant().stream()
    except TypeError:
        return {
            "svc": "prompt-svc",
            "msg": "Could not reach assistant",
            "text": text,
            "history": history,
        }

    return {
        "history": history,
        "prompt": text,
        "answer": answer,
    }


if __name__ == "__main__":
    app.run(host=HOST, post=PORT, debug=True)

# Resources used:
#   - https://medium.com/@abed63/flask-application-with-openai-
#     chatgpt-integration-tutorial-958588ac6bdf
#   - https://medium.com/@jcrsch/openai-assistant-with-flask-
#     a-simple-example-with-code-d007ac42ced2
#
