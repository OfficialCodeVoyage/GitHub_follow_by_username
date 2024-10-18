import os
from datetime import time
from time import sleep
import requests
from fetching_new_users import fetching_users_from_github
import logging
import dotenv
import json
from state_manager import load_state, save_state
from ratelimit import sleep_and_retry, limits
import random
import logging

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("github_follow.log"),
        logging.StreamHandler()
    ]
)

dotenv.load_dotenv()
USERNAMES_FILE = 'usernames.txt'
github_token = os.getenv("GITHUB_TOKEN")# your github token


### read the users from the file
def read_users_from_file():
    with open(USERNAMES_FILE, 'r') as file:
        try:
            users = file.readlines()
            return [user.strip() for user in users]
        except FileNotFoundError as e:
            print(f"Error occurred while reading users from file: {e}")
            return []


### write the users to a file
def write_users_to_file(users):
    with open(USERNAMES_FILE, 'a') as file:
        try:
            existing_users = read_users_from_file()
            for user in users:
                if user not in existing_users:
                    file.write(f"{user}\n")
        except IOError as e:
            print(f"Error occurred while writing users to file: {e}")
        except Exception as e:
            print(f"Error occurred while writing users to file: {e}")


### keep track of last followed user
def read_last_followed_user():
    state = load_state()
    return state.get('last_followed_user', None)


### write the last followed user to a file
def write_last_followed_user(user):
    state = load_state()
    state['last_followed_user'] = user
    save_state(state)


def simple_counter():
    state = load_state()
    state['how_many_bot_followed_so_far_counter'] = state.get('how_many_bot_followed_so_far_counter', 0) + 1
    save_state(state)


### follow the users
ONE_HOUR = 3600
MAX_CALLS_PER_HOUR = 5000
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_HOUR, period=ONE_HOUR)
def follow_users(users):

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Github Follow Script'
    }

    for user in users:
        url = f'https://api.github.com/user/following/{user}'
        try:
            response = requests.put(url, headers=headers)
            print(f"Response status code for {user}: {response.status_code}")
            write_last_followed_user(user)
            simple_counter()
            print("sleeping for 3 second")
            sleep(random.uniform(3, 6))
            if response.status_code == 204:
                logging.info(f"Successfully followed {user}")
            elif response.status_code == 404:
                logging.info(f"User {user} not found")
            elif response.status_code == 429:
                logging.info(f"Rate limit exceeded - Sleeping for 100 seconds")
                sleep(100)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while following {user}: {e}")


def main():
    ### fetch 100 users from GitHub
    try:
        fetched_users = fetching_users_from_github(100, github_token)
        print(fetched_users)
        write_users_to_file(fetched_users)
        logging.info(f"Users written to file: {fetched_users}")
        users = read_users_from_file()
        # logging.info(f"Users read from file: {users}")
        last_user = read_last_followed_user()
        logging.info(f"Last followed user: {last_user}")
        last_user_index = users.index(last_user)
        print(f"Last user index: {last_user_index}")
        users_to_follow = users[last_user_index + 1:]
        print(f"Users to follow: {users_to_follow}")
        follow_users(users_to_follow)
        logging.info(f"Users followed: {users_to_follow}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == '__main__':
    #  I wll be running on VM 24/7, so I will have a while loop
    while True:
        try:
            main()
            print("Sleeping for 90 seconds")
            sleep(90)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            sleep(90)

