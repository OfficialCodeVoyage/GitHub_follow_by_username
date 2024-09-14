# 🚀 GitHub Follow by Username

## 🎉 Introduction

`GitHub Follow by Username` is a Python script that allows you to **follow GitHub users efficiently** by reading their usernames from a file. Leveraging asynchronous programming with `asyncio` and `aiohttp`, this tool manages GitHub's API rate limits gracefully while providing robust logging and resuming capabilities.

## ⭐ Features

- **🔄 Asynchronous Operations:** Utilizes `asyncio` and `aiohttp` for concurrent API requests, enhancing performance.
- **⏱️ Rate Limit Handling:** Dynamically manages GitHub API rate limits by monitoring response headers and implementing backoff strategies.
- **🔁 Resumable Execution:** Tracks the last processed username to allow resuming from where the script left off in case of interruptions.
- **📝 Comprehensive Logging:** Logs detailed information about each follow action, successes, failures, and rate limit statuses to both the console and a log file.
- **🔒 Secure Token Management:** Uses environment variables to handle GitHub Personal Access Tokens (PAT) securely, preventing accidental exposure.
- **⚙️ Concurrency Control:** Limits the number of concurrent API requests to avoid triggering GitHub's abuse detection mechanisms.

## 📦 Installation

### 🛠️ Prerequisites

- **🐍 Python 3.6 or higher**
- **🔑 GitHub Personal Access Token (PAT)**
  - **Scopes Required:** `read:user`, `user:follow`
  - [Creating a PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

### 📜 Steps

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/OfficialCodeVoyage/GitHub_follow_by_username.git
    cd GitHub_follow_by_username
    ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

    ```sh
    python -m venv venv
    # Activate the virtual environment:
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install the Required Python Packages:**

    It's recommended to use a `requirements.txt` file for managing dependencies. Ensure you have a `requirements.txt` file with the following content:

    ```plaintext
    aiohttp
    python-dotenv
    ```

    Then, install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

    **⚠️ Note:** Avoid installing standard library modules like `time` via `pip` as they are already included with Python.

## 🛠️ Usage

### 1. **🔧 Configure Environment Variables**

Create a `.env` file in the root directory of the project to securely store your GitHub PAT and other configurations.

```dotenv
GITHUB_TOKEN=your_github_personal_access_token_here
USERNAMES_FILE=usernames.txt
LAST_LINE_FILE=last_line.txt
```

### 2. 📄 Prepare the Usernames File

Create a file named usernames.txt in the same directory as the script and add the GitHub usernames you want to follow,
one per line. You are welcome to use my file as an example.

### 3. 🚀 Run the Script

```sh
python follow_users.py
```

🔍 Optional Parameters:

If you want to specify a starting line number (useful for resuming), you can modify the .env file:

```dotenv
START_LINE=0# Change to the desired line number (0-indexed)
```
📝 Note: The script automatically resumes from the last processed line by reading the last_line.txt file. Adjusting START_LINE can override this behavior if needed.

## 🔍 Script Details

### 📚 Modules and Dependencies

- **`asyncio` & `aiohttp`:** For asynchronous HTTP requests to the GitHub API.
- **`python-dotenv`:** For loading environment variables from the `.env` file.
- **`logging`:** For comprehensive logging of the script's operations.
- **`os` & `time`:** For environment variable management and handling rate limits.

### 🔑 Key Functions

- **`read_usernames(file_path: str) -> List[str]`:**  
  Reads GitHub usernames from the specified file and returns them as a list.

- **`follow_user(session: aiohttp.ClientSession, username: str) -> Tuple[int, str]`:**  
  Sends a PUT request to the GitHub API to follow the specified user.

- **`handle_rate_limit(headers: dict)`:**  
  Checks the response headers for rate limit information and sleeps if the rate limit has been reached.

- **`write_last_line(file_path: str, line_number: int) -> None`:**  
  Writes the last processed line number to a file to enable resuming.

- **`main()`:**  
  Orchestrates reading usernames, following users asynchronously, handling rate limits, and logging.
handling rate limits, and logging.

## 🤝 Contributing

We welcome contributions from the community! Here’s how you can help:

1. **Fork the Repository.**

2. **Create a New Branch:**

    ```sh
    git checkout -b feature-branch
    ```

3. **Make Your Changes and Commit Them:**

    ```sh
    git commit -m "Add new feature"
    ```

4. **Push to the Branch:**

    ```sh
    git push origin feature-branch
    ```

5. **Open a Pull Request.**

## 🛡️ Security Best Practices

- **🚫 Never Commit `.env` Files:**  
  Ensure that `.env` is listed in `.gitignore` to prevent accidental commits of sensitive information.

- **🔒 Use Git Hooks to Prevent Secret Exposure:**  
  Implement tools like `git-secrets` to scan for sensitive data before allowing commits.

- **🔄 Regularly Rotate Personal Access Tokens (PATs):**  
  Periodically revoke and regenerate PATs to minimize the risk of unauthorized access.

- **👥 Educate Collaborators:**  
  Ensure that all team members are aware of best practices for handling secrets and sensitive information.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📚 Additional Resources

- **📖 GitHub REST API Documentation:**  
  [https://docs.github.com/en/rest](https://docs.github.com/en/rest)

- **🛠️ BFG Repo-Cleaner:**  
  [https://rtyley.github.io/bfg-repo-cleaner/](https://rtyley.github.io/bfg-repo-cleaner/)

- **🔐 GitHub Secret Scanning:**  
  [https://docs.github.com/en/code-security/secret-scanning](https://docs.github.com/en/code-security/secret-scanning)

- **📝 GitHub CLI Documentation:**  
  [https://cli.github.com/manual/](https://cli.github.com/manual/)
