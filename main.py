import os
from datetime import time
from time import sleep
import requests
from fetching_new_users import fetching_users_from_github
import logging
import dotenv
import json
from state_manager import load_state, save_state


dotenv.load_dotenv()
USERNAMES_FILE = 'usernames.txt'
github_token = os.getenv("GITHUB_TOKEN")# your github token


### read the users from the file
def read_users_from_file():
    with open(USERNAMES_FILE, 'r') as file:
        users = file.readlines()
        return [user.strip() for user in users]


### write the users to a file
def write_users_to_file(users):
    with open(USERNAMES_FILE, 'a') as file:
        existing_users = read_users_from_file()
        for user in users:
            if user not in existing_users:
                file.write(f"{user}\n")


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
            sleep(5)
            if response.status_code == 204:
                print(f"Successfully followed {user}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while following {user}: {e}")


def main():
    ### fetch 100 users from GitHub
    fetched_users = fetching_users_from_github(100, github_token)
    print(fetched_users)
    write_users_to_file(fetched_users)
    print("Users written to file")
    users = read_users_from_file()
    print("Users read from file")
    print(users)
    last_user = read_last_followed_user()
    print(f"Last followed user: {last_user}")
    last_user_index = users.index(last_user)
    print(f"Last user index: {last_user_index}")
    users_to_follow = users[last_user_index + 1:]
    print(f"Users to follow: {users_to_follow}")
    follow_users(users_to_follow)
    print("Users followed")


if __name__ == '__main__':
    #  I wll be running on VM 24/7, so I will have a while loop
    while True:
        main()
        print("Sleeping for 1 hour")
        sleep(90)


