import datetime
import pandas as pd


from helpers import (
    get_credentials_from_secret_manager,
    get_access_token_spotify,
    search_for_podcasts_spotify,
    extract_episodes_from_show_spotify
)


def orchestrate():
    dfs = {}
    while True:
        try:
            # Get Client ID and Client Secret
            credentials = get_credentials_from_secret_manager()
            client_id = credentials["spotify"]["client_id"]
            client_secret = credentials["spotify"]["client_secret"]
