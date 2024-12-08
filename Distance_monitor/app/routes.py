# app/routes.py
from flask import Blueprint, render_template, jsonify
from app.serial_handler import get_sensor_data

main = Blueprint('main', __name__)

@main.route('./')
def index():
    return render_template('templates/index.html')

@main.route('/data')
def get_data():
    return jsonify(get_sensor_data())