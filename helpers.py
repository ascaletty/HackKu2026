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


autocomp = input("Input your addy")
# print(autocomplete(autocomp))
# #
print(forwardGeocode(autocomp))

# def reverseGeocode(coordinates):
# probably won't need this thing I don't think
