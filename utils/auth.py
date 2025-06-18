import requests
import yaml

def get_oauth_token(environment):
    with open('config/test_data.yaml', 'r') as file:
        config = yaml.safe_load(file)

    oauth_config = config['oauth']
    api_scope = config['environments'][environment]['api_scope']

    response = requests.post(oauth_config['token_url'], data={
        'grant_type': oauth_config['grant_type'],
        'client_id': oauth_config['client_id'],
        'client_secret': oauth_config['client_secret'],
        'scope': api_scope
    })

    response.raise_for_status()
    return response.json()['access_token']
