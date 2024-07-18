from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

web_bp = Blueprint('web', __name__,
                   static_folder='../web/static',
                   template_folder='templates')


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

# Resource(s) Used:
# https://flask.palletsprojects.com/en/3.0.x/blueprints/
