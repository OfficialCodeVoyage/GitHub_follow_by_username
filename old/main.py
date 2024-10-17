import asyncio
import aiohttp
import time
import os
import logging
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO for general logs; use DEBUG for more verbosity
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("../follow_users.log"),
        logging.StreamHandler()
    ]
)

# Constants
USERNAMES_FILE = os.getenv('USERNAMES_FILE', 'usernames.txt')
LAST_LINE_FILE = os.getenv('LAST_LINE_FILE', '../last_line.txt')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    logging.error("GitHub token not found. Please set GITHUB_TOKEN in the environment variables.")
    exit(1)

# Semaphore to limit concurrent requests (set to 1 for sequential processing)
SEM = asyncio.Semaphore(1)

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
async def follow_user(session: aiohttp.ClientSession, username: str, line_number: int) -> None:
    url = f'https://api.github.com/user/following/{username}'
    async with SEM:  # Ensure sequential processing
        try:
            async with session.put(url) as response:
                status = response.status
                text = await response.text()

                if status == 204:
                    logging.info(f"Line {line_number + 1}: Successfully followed '{username}'.")
                elif status == 404:
                    logging.warning(f"Line {line_number + 1}: User '{username}' not found.")
                elif status == 403 or status == 429:
                    logging.error(f"Line {line_number + 1}: Rate limit exceeded or forbidden access.")
                else:
                    logging.error(f"Line {line_number + 1}: Failed to follow '{username}': {status}, {text}")

        except Exception as e:
            logging.exception(f"Line {line_number + 1}: Error following user '{username}': {e}")

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
            await follow_user(session, username, i)

            # Wait for 10 seconds before processing the next user
            if i < total_usernames - 1:
                #logging.info("Waiting for 10 seconds before following the next user...")
                await asyncio.sleep(10)

            # Update the last processed line
            write_last_line(LAST_LINE_FILE, i + 1)

    logging.info("Finished processing all usernames.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
