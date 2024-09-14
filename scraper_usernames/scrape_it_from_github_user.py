import dotenv
import requests
from time import sleep
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your GitHub username and token
username = dotenv.get("USERNAME")  # The GitHub username to scrape
token = dotenv.get("GITHUB_TOKEN")  # The personal access token to authenticate to the GitHub API

# GitHub API endpoint and headers
api_url = f"https://api.github.com/users/{username}/following"
headers = {"Authorization": f"token {token}"}

# Initialize variables
following_users = []
start_user_number = 107001  # Change this to the user number to start from
per_page = 100  # Max is 100
start_page = start_user_number // per_page + 1  # Calculate the starting page
start_index = start_user_number % per_page  # Calculate the index on that page
collected_count = 0
save_interval = 1000
rate_limit_remaining = 5000

# File name to store usernames
file_name = "following_users.txt"

# Check if file exists and count the number of existing lines
if os.path.exists(file_name):
    with open(file_name, "r") as file:
        existing_lines = len(file.readlines())
else:
    existing_lines = 0

# Set starting line for saving
start_line = existing_lines + 1

# Start scraping from the calculated page and index
page = start_page

while True:
    # API request to fetch following users
    response = requests.get(api_url, headers=headers, params={"per_page": per_page, "page": page})
    data = response.json()

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json()}")
        break

    if not data:
        # No more data, break the loop
        break

    # Process data starting from the desired index
    if page == start_page:
        data = data[start_index:]

    # Extract usernames and add to the list
    following_users.extend([user["login"] for user in data])
    collected_count += len(data)

    # Save usernames every 1000 users
    if collected_count >= save_interval:
        with open(file_name, "a") as file:
            for user in following_users:
                file.write(user + "\n")
        print(f"{len(following_users)} usernames saved to {file_name} starting from line {start_line}")
        start_line += len(following_users)
        following_users.clear()
        collected_count = 0

    # Handle rate limit
    rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
    if rate_limit_remaining <= 1:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        sleep_time = max(reset_time - int(time.time()), 0)
        print(f"Rate limit hit. Sleeping for {sleep_time} seconds.")
        sleep(sleep_time + 1)  # Wait until the rate limit resets
        continue

    # Print progress
    print(f"Page {page} fetched. Total users collected: {collected_count}")

    # Increment page for next API request
    page += 1

    # Respectful delay between requests to avoid hitting rate limits too quickly
    sleep(10)

# Save any remaining usernames after the loop ends
if following_users:
    with open(file_name, "a") as file:
        for user in following_users:
            file.write(user + "\n")
    print(f"Remaining {len(following_users)} usernames saved to {file_name} starting from line {start_line}")
