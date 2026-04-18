from requests import request
from flask import render_template
from flask import Flask, request
from helpers import forwardGeocode, calc_route

app = Flask(__name__)


@app.route("/")
def hello(name=None):
    return render_template("hello.html", person=name)


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
    print(route_json)
    coords = [[coords1[1], coords1[0]], [coords2[1], coords2[0]], route_cords]
    return coords
