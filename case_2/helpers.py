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
