from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from inspect import cleandoc as clean
import requests
import os

web_bp = Blueprint('web', __name__,
                   static_folder='../web/static',
                   template_folder='templates')


ERROR_MESSAGE_400 = {"Error": "The request body is invalid"}

PROMPT_SVC = os.getenv('PROMPT_SVC')


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

    print(request.args)
    # get json body from POST request
    content = request.args
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
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": clean(
                        """You are a professional vacation planner helping
                        users plan trips abroad. You will recommend hotels,
                        attractions, restaurants, shopping area, natural
                        sites or any other places that the user requests.
                        You will plan according to the budget and vacation
                        length given by the user. You will present the
                        result in a format of detailed itinerary of each
                        day, begin from day 1 to the last day."""
                    )
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": clean(
                        f"""Plan me a {days_num} days trip to {destination}.
                        This is for a party of {travelers_num} adults aging
                        from 35-38. We are interested in visiting shopping
                        area, enjoying local food, with a one or two night
                        life. We will strictly stay in Tokyo. Budget should
                        be $1500 per person without airfare, but include
                        ehotels, meals and other xpenses. We will be
                        leaving from New York, USA. {travel_preference}"""
                    )
                }
            ]
        }
    ]

    print(messages)

    response = promptServiceChat(messages)
    print(response)
    return response.json()


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


def promptServiceChat(messages):
    return requests.post(PROMPT_SVC + '/v1/prompt/itinerary',
                         json={"messages": messages})

# Resource(s) Used:
# https://flask.palletsprojects.com/en/3.0.x/blueprints/
