import requests
from requests.structures import CaseInsensitiveDict
from dotenv import dotenv_values

# url = "https://api.geoapify.com/v1/geocode/search?text=38%20Upper%20Montagu%20Street%2C%20Westminster%20W1H%201LJ%2C%20United%20Kingdom&apiKey=f9ea11b86f7c43578f59ef64ee700550"
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
    # url = "https://api.geoapify.com/v1/geocode/autocomplete?text=Lessingstra%C3%9Fe%203%2C%20Regensburg&format=json&apiKey=d548c5ed24604be6a9dd0d989631f783"
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
def routingtoGeoJson(coordinates):


# autocomp = input("Input your addy")
# print(autocomplete(autocomp))
# #
# print(forwardGeocode(autocomp))

# def reverseGeocode(coordinates):
# probably won't need this thing I don't think
