import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = os.environ.get("BEARER_TOKEN")

bearer_token = "AAAAAAAAAAAAAAAAAAAAAN6ubQEAAAAAsskOd3YAHJYaqf666eJGJmraaM0%3DLGe7PDtgFvFfqdWubiMNnfs9H1Nr1KpJuyZ9khmbQgFLlEbW5l"


def create_url(id):
    # Replace with user ID below
    user_id = id
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)


def get_params():
    return {"user.fields": "created_at,profile_image_url", "max_results": 100}

def get_params_pagination(pagination_token):
    return {"user.fields": "created_at,profile_image_url", "max_results": 100, "pagination_token": pagination_token}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_data(id):
    url = create_url(id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    

    return json_response


if __name__ == "__main__":
    get_data()