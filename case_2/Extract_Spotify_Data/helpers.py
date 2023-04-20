import json
import requests
import pandas as pd

from google.cloud import secretmanager


def get_credentials_from_secret_manager(
    project_name="gbo-case2", secrets_name="gbo-spotify-credentials", version=1
):

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_name}/secrets/{secrets_name}/versions/{version}"
    payload = client.access_secret_version(request={"name": name}).payload
    credentials = eval(payload.data.decode("utf-8"))
    return credentials


def get_access_token_spotify(url, client_id, client_secret):
    payload=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['access_token']


def search_for_podcasts_spotify(url, access_token):
    payload={}
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)


def extract_episodes_from_show_spotify(url, access_token):
    episodes = pd.DataFrame()
    while True:
        try:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            params = {
                "market": "BR",
                "limit": 50,
                "offset": 0
            }

            response = requests.get(url, headers=headers, params=params)

            df = pd.json_normalize(
                json.loads(response.text)['items']
            )

            episodes = pd.concat([
                episodes
                , df
            ])

            if json.loads(response.text)['next'] != "":
                url = json.loads(response.text)['next']
            
        except:
            break
    return episodes
