import asyncio
import aiohttp
import time
import os
import logging
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("follow_users.log"),
        logging.StreamHandler()
    ]
)

# Constants
USERNAMES_FILE = os.getenv('USERNAMES_FILE', 'usernames.txt')
LAST_LINE_FILE = os.getenv('LAST_LINE_FILE', 'last_line.txt')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    logging.error("GitHub token not found. Please set GITHUB_TOKEN in the environment variables.")
    exit(1)

# Semaphore to limit concurrent requests
SEM = asyncio.Semaphore(5)  # Adjust the number based on your needs and testing

# Function to read usernames from a file
def read_usernames(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
        logging.info(f"Loaded {len(usernames)} usernames from '{file_path}'.")
        return usernames
    except FileNotFoundError:
        logging.error(f"Usernames file '{file_path}' not found.")
        exit(1)
    except Exception as e:
        logging.exception(f"An error occurred while reading '{file_path}': {e}")
        exit(1)

# Function to read the last processed line number
def read_last_line(file_path: str) -> int:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                last_line = int(file.read().strip())
            logging.info(f"Resuming from line {last_line + 1}.")
            return last_line
        except ValueError:
            logging.warning(f"Invalid content in '{file_path}'. Starting from the beginning.")
            return 0
        except Exception as e:
            logging.exception(f"An error occurred while reading '{file_path}': {e}")
            return 0
    logging.info(f"No last line file found. Starting from the beginning.")
    return 0

# Function to write the last processed line number
def write_last_line(file_path: str, line_number: int) -> None:
    try:
        with open(file_path, 'w') as file:
            file.write(str(line_number))
        logging.debug(f"Updated last line to {line_number} in '{file_path}'.")
    except Exception as e:
        logging.exception(f"An error occurred while writing to '{file_path}': {e}")

# Asynchronous function to follow a user on GitHub
async def follow_user(session: aiohttp.ClientSession, username: str) -> Tuple[int, str]:
    url = f'https://api.github.com/user/following/{username}'
    async with SEM:  # Limit concurrency
        try:
            async with session.put(url) as response:
                status = response.status
                text = await response.text()

                # Log rate limit headers
                rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
                rate_limit_reset = response.headers.get('X-RateLimit-Reset')
                if rate_limit_remaining and rate_limit_reset:
                    logging.debug(f"Rate Limit Remaining: {rate_limit_remaining}")
                    logging.debug(f"Rate Limit Reset Time: {rate_limit_reset}")

                return status, text
        except Exception as e:
            logging.exception(f"Error following user '{username}': {e}")
            return 0, str(e)

# Function to handle rate limiting based on GitHub's response headers
async def handle_rate_limit(headers: dict):
    rate_limit_remaining = headers.get('X-RateLimit-Remaining')
    rate_limit_reset = headers.get('X-RateLimit-Reset')

    if rate_limit_remaining is not None and rate_limit_reset is not None:
        rate_limit_remaining = int(rate_limit_remaining)
        rate_limit_reset = int(rate_limit_reset)

        if rate_limit_remaining == 0:
            current_time = int(time.time())
            sleep_duration = rate_limit_reset - current_time + 5  # Add a buffer of 5 seconds
            if sleep_duration > 0:
                reset_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rate_limit_reset))
                logging.warning(f"Rate limit reached. Sleeping until {reset_time_str} ({sleep_duration} seconds).")
                await asyncio.sleep(sleep_duration)

# Function to check and handle rate limits after each request
async def check_rate_limit_after_request(response: aiohttp.ClientResponse):
    headers = response.headers
    await handle_rate_limit(headers)

# Main asynchronous function
async def main():
    usernames = read_usernames(USERNAMES_FILE)
    last_line = read_last_line(LAST_LINE_FILE)
    total_usernames = len(usernames)
    logging.info(f"Starting to follow users from line {last_line + 1} to {total_usernames}.")

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Follow-Script'  # Replace with your application's name
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for i, username in enumerate(usernames[last_line:], start=last_line):
            status_code, response_text = await follow_user(session, username)

            if status_code == 204:
                logging.info(f"Line {i + 1}: Successfully followed '{username}'.")
                write_last_line(LAST_LINE_FILE, i + 1)
            elif status_code == 404:
                logging.warning(f"Line {i + 1}: User '{username}' not found.")
                write_last_line(LAST_LINE_FILE, i + 1)
            elif status_code == 403:
                if 'rate limit' in response_text.lower():
                    logging.error(f"Line {i + 1}: Rate limit exceeded.")
                    # Extract headers from the last response
                    await handle_rate_limit(session._connector._session.headers)
                else:
                    logging.error(f"Line {i + 1}: Forbidden access when trying to follow '{username}'.")
            else:
                logging.error(f"Line {i + 1}: Failed to follow '{username}': {status_code}, {response_text}")

            # Optional: Dynamic sleep based on remaining rate limit
            # This example uses a fixed sleep; you can adjust it based on rate limits
            await asyncio.sleep(1)  # Adjust as needed

    logging.info("Finished processing all usernames.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
