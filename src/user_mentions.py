import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = os.environ.get("BEARER_TOKEN")

bearer_token = "AAAAAAAAAAAAAAAAAAAAAN6ubQEAAAAAsskOd3YAHJYaqf666eJGJmraaM0%3DLGe7PDtgFvFfqdWubiMNnfs9H1Nr1KpJuyZ9khmbQgFLlEbW5l"


def create_url(user_id):
    return "https://api.twitter.com/2/users/{}/mentions".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,author_id", "max_results": 100}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserMentionsPython"
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


def get_data(user_id):
    url = create_url(user_id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)

    user_mentions = {}
    
    for mention in json_response["data"]:
        author_id = mention["author_id"]
        if author_id in user_mentions.keys():
            value = user_mentions[author_id]
            user_mentions[author_id] = value + 1
        else:
            user_mentions[author_id] = 1

    json_response.pop("data")
    json_response.pop("meta")
    if user_mentions:
        json_response['user_mentions'] = user_mentions


    #print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response


if __name__ == "__main__":
    get_data()