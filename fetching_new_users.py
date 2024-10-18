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
    current_page = state.get('current_page', 0)

    querry = 'language:python repos:>5 followers:>10'
    url = "https://api.github.com/search/users"
    params = {
        'per_page': users_to_fetch,
        'page': current_page,
        'q': querry

    }
    headers = {
        'Authorization': token,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Github Follow Script'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        fetched_users_api = data.get('items', [])
        fetched_users = [user['login'] for user in fetched_users_api]
        state['current_page'] = current_page + 1
        save_state(state)


    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return fetched_users
