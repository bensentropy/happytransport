# -*- coding: UTF-8 -*-

from core import app
from google.appengine.api import urlfetch
from flask import render_template, request
from core.happy import HappyTravellerMetricsBS
from core.distance import get_output

urlfetch.set_default_fetch_deadline(120)


@app.route("/")
def home():
    return render_template(
        'home.html',
    )

@app.route("/calculate", methods=['POST', 'GET'])
def calculate():
    origin = request.form['from']
    destination = request.form['to']

    # Distance
    departure_time = '1343641500'  # TODO is this correct?

    distances = get_output(origin, destination, departure_time)

    # health benefits
    htmbs = HappyTravellerMetricsBS()

    daily_km_walked = float(distances['transit']['distance_walking']) * 2 / 1000
    daily_walking_hours = float(distances['transit']['time_walking']) / 60 / 60 * 2
    weight = int(request.form['weight'])
    height = float(request.form['height']) / 100

    health_benefits = htmbs.get_health_benefits(
        daily_km_walked, daily_walking_hours, weight, height)

    # car costs

    daily_car_commute_km = float(distances['driving']['distance']) * 2 / 1000
    daily_parking_cost = int(request.form['parking'])
    engine_size = request.form['engine_size']
    daily_pt_cost = distances['transit']['cost'] * 2

    yearly_money_savings = htmbs.get_yearly_money_saving(
        daily_car_commute_km, daily_parking_cost, engine_size, daily_pt_cost)

    # Environment
    car_fuel_type = 'petrol'  # TODO: put this in the user interface
    environmental_benefits = htmbs.get_environmental_benefits(daily_car_commute_km, car_fuel_type)

    # Time use benefits
    daily_car_use_hours = float(distances['driving']['time']) * 2 / 60 / 60
    daily_pt_vehicle_hours = float(distances['transit']['time_transit']) * 2 / 60 / 60
    daily_pt_total_hours = float(distances['transit']['time']) * 2 / 60 / 60

    time_use_benefits = htmbs.get_time_use_benefits(daily_car_use_hours, daily_pt_vehicle_hours, daily_pt_total_hours)

    return render_template(
        'calculate.html',
        instructions=distances['transit']['instructions'].replace('\n', '<br>'),
        health_benefits=health_benefits,
        yearly_money_savings=yearly_money_savings,
        environmental_benefits=environmental_benefits,
        time_use_benefits=time_use_benefits
    )


def year_convert(value):
    days_worked_per_year = 217
    return value * days_worked_per_year