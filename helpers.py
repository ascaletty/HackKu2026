import re
from collections import defaultdict
import datetime
import time
import numpy as np
import requests
from requests.structures import CaseInsensitiveDict
from dotenv import dotenv_values

config = dotenv_values(".env")


def forwardGeocode(addy):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    url = "https://api.geoapify.com/v1/geocode/search?text="
    addy.replace(" ", "%20")
    url = url + addy + "&apiKey=" + config["API_KEY"]
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(resp.status_code)
        resp_json = resp.json()
        return resp_json
    else:
        raise ValueError(
            f"server returned exit code {resp.status_code} with {resp.json()}"
        )


def autocomplete(addy):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    url = "https://api.geoapify.com/v1/geocode/autocomplete?text="
    addy.replace(" ", "%20")
    url = url + addy + "&apiKey=" + config["API_KEY"]
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(resp.status_code)
        resp_json = resp.json()
        return resp_json
    else:
        raise ValueError(
            f"server returned exit code {resp.status_code} with {resp.json()}"
        )


def calc_route(source, destination):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    print(source)
    print(destination)
    url = (
        "https://api.geoapify.com/v1/routing?waypoints="
        + str(source[1])
        + ","
        + str(source[0])
        + "|"
        + str(destination[1])
        + ","
        + str(destination[0])
        + "&mode=drive&apiKey="
        + config["API_KEY"]
    )
    print(url)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(resp.status_code)
        resp_json = resp.json()
        # print(resp_json)
        # get_route_forecast(resp_json)
        return resp_json
    else:
        raise ValueError(
            f"server returned exit code {resp.status_code} with {resp.json()}"
        )


def get_route_forecast(route, leaving_time):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    path = route["features"][0]["geometry"]["coordinates"]

    legs = route["features"][0]["properties"]["legs"][0]["steps"]
    # print(legs)

    # now = time.time()
    now = leaving_time
    dt = datetime.datetime.fromtimestamp(now)
    future_hour = 0
    hour = dt.hour
    dict_path = defaultdict(dict)
    for leg in legs:
        now += float(leg["time"])
        print(leg)
        num = leg["to_index"]
        dtn = datetime.datetime.fromtimestamp(now)
        print(f" now {dtn.hour} and hour {hour}")
        if dtn.hour > hour:
            hour += 1
            future_hour += 1
            print("HOUR UP  \n")
        gridpoints = (
            "https://api.weather.gov/points/"
            + str(path[0][int(num)][1])
            + ","
            + str(path[0][int(num)][0])
        )

        resp = requests.get(gridpoints, headers=headers)
        resp = resp.json()
        forecast = get_grid_coord_forecast(resp)
        dict_path[leg["to_index"]][now] = forecast["properties"]["periods"][future_hour]

    print(dict_path)

    # length = len(path[0])
    # avg_path = np.linspace(0, length - 1, 20)
    # for num in avg_path:
    #     gridpoints = (
    #         "https://api.weather.gov/points/"
    #         + str(path[0][int(num)][1])
    #         + ","
    #         + str(path[0][int(num)][0])
    #     )
    #
    #     resp = requests.get(gridpoints, headers=headers)
    #     resp = resp.json()
    #     get_grid_coord_forecast(resp)
    #


def get_grid_coord_forecast(resp):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    cwa = resp["properties"]["cwa"]
    x = resp["properties"]["gridX"]
    y = resp["properties"]["gridY"]

    forecastUrl = (
        "https://api.weather.gov/gridpoints/"
        + cwa
        + "/"
        + str(x)
        + ","
        + str(y)
        + "/forecast/hourly?units=us"
    )
    resp2 = requests.get(forecastUrl, headers=headers)
    resp2 = resp2.json()
    # print(
    #     f"it will be {resp2['properties']['periods'][0]['temperature']} from {resp2['properties']['periods'][0]['startTime']} to {resp2['properties']['periods'][0]['endTime']}"
    # )
    return resp2


# autocomp = input("Input your addy")
# # print(autocomplete(autocomp))
# # #
# print(forwardGeocode(autocomp))

# def reverseGeocode(coordinates):
# probably won't need this thing I don't think
