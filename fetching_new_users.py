import os
import requests
import dotenv


dotenv.load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")# your github token


def fething_users_from_github(users_to_fetch=1, token=None) -> list:
    scraped_users = []

    querry = 'language:python repos:>5 followers:>10'
    url = "https://api.github.com/search/users"
    params = {
        'per_page': users_to_fetch,
        'since': 0,
        'q': querry

    }
    headers = {
        'Authorization': token
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        users = response.json().get('items', [])

        for user in users:
            scraped_users.append(user['login'])

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return scraped_users
