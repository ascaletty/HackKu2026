from requests import request
import requests
from flask import render_template
from flask import Flask, request
from helpers import forwardGeocode, calc_route, get_route_forecast

app = Flask(__name__)
data = {}


@app.route("/", methods=["POST", "GET"])
def hello():
    return render_template("hello.html")


@app.route("/form", methods=["POST"])
def form_api():
    addy1 = request.form.get("addy1")
    addy2 = request.form.get("addy2")
    resp1 = forwardGeocode(addy1)
    resp2 = forwardGeocode(addy2)
    coords1 = resp1["features"][0]["geometry"]["coordinates"]

    coords2 = resp2["features"][0]["geometry"]["coordinates"]
    route_json = calc_route(coords1, coords2)
    coords = route_json["features"][0]["geometry"]["coordinates"]
    route_cords = [(lat, lon) for segment in coords for lon, lat in segment]
    # print(route_json)
    temp_time_dict = get_route_forecast(route_json)
    print(temp_time_dict)
    coords = [
        [coords1[1], coords1[0]],
        [coords2[1], coords2[0]],
        route_cords,
        temp_time_dict,
    ]
    return coords


# @app.route("/weather", methods=["POST"])
# def weather(name=None):
#     weather_source = request.form.get("source")
#     return render_template("weather.html", person=name)
