from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from inspect import cleandoc as clean
import requests
import json
import os

web_bp = Blueprint('web', __name__,
                   static_folder='../web/static',
                   template_folder='templates')

ERROR_MESSAGE_400 = {"Error": "The request body is invalid"}

PROMPT_SVC_HOST = os.getenv('PROMPT_SVC_HOST')
PROMPT_SVC_PORT = os.getenv('PROMPT_SVC_PORT')

@web_bp.route('/', methods=['GET'])
def home():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@web_bp.route('/plan-a-trip', methods=['GET'])
def plan_a_trip():
    try:
        return render_template('plan-a-trip.html')
    except TemplateNotFound:
        abort(404)


@web_bp.route('/plan-a-trip', methods=['POST'])
def plan_a_trip_post():

    # get json body from POST request
    content = request.form
    # contact prompt-svc
    gpt_response = promptServiceInitialReq(content)
    return render_template('plan-a-trip.html', gpt_response=gpt_response)


@web_bp.route('/recommendations', methods=['GET'])
def recommendations():
    try:
        return render_template('recommendations.html')
    except TemplateNotFound:
        abort(404)


@web_bp.route('/login-method', methods=['GET'])
def login_method():
    try:
        return render_template('login-method.html')
    except TemplateNotFound:
        abort(404)

###########################################################
#
#  Route to use promt-svc's initial GPT request route
#
#  Receives:
#   - content:  variables from UI's form
#
#  Returns:
#   - gpt_message:  string
#
###########################################################
def promptServiceInitialReq(content):
    r = requests.post('http://' + PROMPT_SVC_HOST + ':' + PROMPT_SVC_PORT + '/v1/prompt/initial-req',
                         json=content)
    response = r.json()
    gpt_message = response['gpt-message']
    return gpt_message
    
def promptServiceChat(messages):
    return requests.post('http://' + PROMPT_SVC_HOST + ':' + PROMPT_SVC_PORT + '/v1/prompt/itinerary',
                         json={"messages": messages})

# Resource(s) Used:
# https://flask.palletsprojects.com/en/3.0.x/blueprints/
