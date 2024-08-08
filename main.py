import requests
import time
import os


def read_usernames(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def follow_user(username, headers):
    response = requests.put(f'https://api.github.com/user/following/{username}', headers=headers)
    return response.status_code, response.text


def main(file_path, token, start_line):
    usernames = read_usernames(file_path)
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Start from the specified line
    for i, username in enumerate(usernames[start_line:], start=start_line):
        status_code, response_text = follow_user(username, headers)
        if status_code == 204:
            print(f'Line {i + 1}: Successfully followed {username}')
        else:
            print(f'Line {i + 1}: Failed to follow {username}: {status_code}, {response_text}')
        time.sleep(15)  # To avoid hitting rate limits


if __name__ == "__main__":
    FILE_PATH = 'usernames.txt'  # Path to the usernames
    TOKEN = os.getenv('GITHUB_TOKEN')  # Your GitHub personal access token ---> Settings ---> Dev. Settings ---> Personal Access Token
    START_LINE = 10223 # The line number to start from (0-indexed)

    main(FILE_PATH, TOKEN, START_LINE)
