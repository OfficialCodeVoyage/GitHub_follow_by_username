# fetching_new_users.py = only getting 100 new users for each iteration

import os
import requests
import dotenv
from typing import List
from state_manager import load_state, save_state

dotenv.load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")  # your github token


def fetching_users_from_github(users_to_fetch=100, token=None) -> List[str]:

    state = load_state()
    last_fetched_user = state.get('last_fetched_user', None)

    querry = 'language:python repos:>2 followers:>10'
    url = "https://api.github.com/users"
    params = {
        'per_page': users_to_fetch,
        'since': last_fetched_user

    }
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Github Follow Script'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        fetched_users_api = response.json()
        fetched_users = [user['login'] for user in fetched_users_api]


        last_fetched_user = fetched_users_api[-1]['id']
        state['last_fetched_user'] = last_fetched_user
        save_state(state)


    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return fetched_users

