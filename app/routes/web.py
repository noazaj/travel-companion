from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
import requests
import os
# import threading
import json

web_bp = Blueprint('web', __name__,
                   static_folder='../web/static',
                   template_folder='templates')

ERROR_MESSAGE_400 = {"Error": "The request body is invalid"}
notification_update = {}
get_itinerary_data = {}
get_weather_data = {}

PROMPT_SVC_URL = os.getenv('PROMPT_SVC_URL')


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
    # Get form data
    content = request.form
    destination = content.get('destination')

    # Contact prompt-svc for trip planning
    gpt_response = promptServiceInitialReq(content)

    # Fetch weather update for the destination
    fetch_weather_update(destination)
    itinerary_data_out = generate_itinerary_data(get_itinerary_data)

    return render_template('plan-a-trip.html',
                           gpt_response=gpt_response,
                           notification_update=notification_update,
                           itinerary_data=itinerary_data_out)


@web_bp.route('/chat-plan-a-trip', methods=['POST'])
def plan_a_trip_chat():
    content = request.get_json()
    message = content.get('message')

    if not message:
        return jsonify(ERROR_MESSAGE_400), 400

    gpt_chat_response = promptServiceChat({"message": message})

    return jsonify({'gpt_chat_response': gpt_chat_response})


@web_bp.route('/recommendations', methods=['GET'])
def recommendations():
    try:
        weather_data = generate_weather_data(get_weather_data)
        itinerary_data_out = generate_itinerary_data(get_itinerary_data)
        return render_template('recommendations.html',
                               notification_update=notification_update,
                               weather_data=weather_data,
                               itinerary_data=itinerary_data_out,
                               promptUrl=promptSvcUrl())
    except TemplateNotFound:
        abort(404)


@web_bp.route('/login-method', methods=['GET'])
def login_method():
    try:
        return render_template('login-method.html')
    except TemplateNotFound:
        abort(404)


@web_bp.route('/profile', methods=['GET'])
def profile():
    try:
        return render_template('profile.html')
    except TemplateNotFound:
        abort(404)


@web_bp.route('/profile', methods=['POST'])
def profile_post():

    # Get form data
    content = request.form
    age = content.get('age')
    travelStyle = content.get('travel-style')
    travelPriorities = content.get('travel-priorities')
    travelAvoidances = content.get('travel-avoidances')
    dietaryRestrictions = content.get('dietary-restrictions')
    accomodations = content.get('accomodations')

    # Save to database

    # Fetch from database and reload profile

    try:
        return render_template('profile.html',
                               age=age,
                               travelStyle=travelStyle,
                               travelPriorities=travelPriorities,
                               travelAvoidances=travelAvoidances,
                               dietaryRestrictions=dietaryRestrictions,
                               accomodations=accomodations)
    except TemplateNotFound:
        abort(404)


@web_bp.route('/get-notification', methods=['GET'])
def get_notification():
    return jsonify(notification_update)


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

    r = requests.post(f'{promptSvcUrl()}/v1/prompt/initial-trip-planning-req',

                      json=content)
    response = r.json()
    gpt_message = response['gpt-message']
    global get_itinerary_data
    get_itinerary_data = gpt_message
    return gpt_message


def promptServiceChat(content):

    r = requests.post(f'{promptSvcUrl()}/v1/prompt/trip-planning-chat',
                      json=content)
    response = r.json()
    print(response)
    gpt_chat_message = response['messages']
    return gpt_chat_message


def fetch_weather_update(location):
    global notification_update
    global get_weather_data

    weather_payload = {"location": location}

    url = f'{promptSvcUrl()}/v1/prompt/weather'

    r = requests.post(url, json=weather_payload)

    if r.status_code == 200:
        data = r.json()
        location = data.get("location", "Unknown location")
        get_weather_data = data.get("weather-update",
                                    "No weather update available")
        notification_update = {
            'message': f"{get_weather_data}",
            'link': '/recommendations'
        }


def promptSvcUrl():
    return PROMPT_SVC_URL


def generate_weather_data(weather_data):
    return json.loads(f"{weather_data}")


def generate_itinerary_data(agenda_data):
    return json.loads(f"{agenda_data}")

# Resource(s) Used:
# https://flask.palletsprojects.com/en/3.0.x/blueprints/
