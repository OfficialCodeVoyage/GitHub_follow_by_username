import os
from datetime import time

import requests
from fetching_new_users import fething_users_from_github
import logging
import dotenv


dotenv.load_dotenv()
USERNAMES_FILE = 'usernames.txt'
LAST_LINE_FILE = 'last_line.txt'
github_token = os.getenv("GITHUB_TOKEN")# your github token

### fetch 100 users from github

users = fething_users_from_github(100, github_token)

### write the users to a file
def write_users_to_file(users):
    with open(USERNAMES_FILE, 'w') as file:
        for user in users:
            file.write(f"{user}\n")

### read the users from the file

### follow the users

### mark the last user followed

### repeat the process - main loop

def main():
    while True:
        users = fething_users_from_github(100, github_token)
        write_users_to_file(users)
        logging.info(f"Following {len(users)} users.")
        logging.info(f"Waiting for 10 minutes...")
        time.sleep(600)