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
            
            # Get access token
            url = "https://accounts.spotify.com/api/token"
            access_token = get_access_token_spotify(url, client_id, client_secret)

            # Get the first 50 podcasts that contains "data hackers"
            searched_term = "data hackers"
            searched_type = "show"
            limit = "50"
            market = "BR"
            url = f"https://api.spotify.com/v1/search?q={searched_term}&type={searched_type}&limit={limit}&market={market}"
            
            dfs['first_50_data_hackers_podcasts'] = search_for_podcasts_spotify(url, access_token)  
            
            dfs['first_50_data_hackers_podcasts'] = pd.json_normalize(
                dfs['first_50_data_hackers_podcasts']['shows']['items']
                )[[
                    'name'
                    , 'description'
                    , 'id'
                    , 'total_episodes'
                ]]    

            # Get all episodes by Data Hackers
            data_hackers_id_spotify = '1oMIHOXsrLFENAeM743g93'
            url = f"https://api.spotify.com/v1/shows/{data_hackers_id_spotify}/episodes"
            dfs['data_hackers_episodes'] = extract_episodes_from_show_spotify(url, access_token)

            dfs['data_hackers_episodes'] = dfs['data_hackers_episodes'][[
                'id'
                , 'name'
                , 'description'
                , 'release_date'
                , 'duration_ms'
                , 'language'
                , 'explicit'
                , 'type'
            ]]

            # Write dataframes on GCS as CSVs
            bucket = "raw-data-gbo/spotify"
            createdAt = datetime.date.today()
            
            for key in list(dfs.keys()):
                dfs[key].to_csv(f"gs://{bucket}/{key}-{createdAt}", index=None, header=True)
                dfs[key].to_csv(f"gs://{bucket}/{key}", index=None, header=True)
            return True

        except Exception:
            return False
        