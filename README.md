# 🚀 GitHub Automation Follower Bot

## 🎉 Introduction

The GitHub Automation Follower Bot is a fully automated tool designed to streamline the process of discovering and following GitHub users based on specific criteria. The goal of this bot to follow **1 000 000** users on Github based on your criteria! 

You have two options to run the script:

1. **Run on your local machine:** Ideal for testing and short-term usage.
[Jump to Installation on local machine](#-installation-on-local-machine)

3. **Set up a Virtual Machine (VM) to run 24/7:** Recommended to maximize the effect by continuously running the bot without interruption.
[Go to Installation on VM](#-installation-on-virtual-machinevm)


## ⭐ New Features

- **🤖 Automated User Scraping:** Transitioned from manual user lists to automated scraping using the GitHub API, eliminating the need for manual updates.
- **💾 Automated State Management:** Introduced state management with `state.json` to persist progress and ensure smooth resumption after interruptions.
- **🖥️ 24/7 VM Deployment:** Optimized for continuous operation on a virtual machine, allowing the bot to run around the clock without manual restarts.

## 📁 File Descriptions

- **`main.py`:** The entry point of the bot. It orchestrates the main flow, handles logging, and ensures continuous operation with a `while True` loop.
- **`fetching_new_users.py`:** Fetches a specified number of new GitHub users based on criteria using the GitHub API.
- **`state_manager.py`:** Manages the loading and saving of the bot's state, ensuring progress is saved and can be resumed.
- **`state.json`:** A JSON file that stores information such as the last followed user and tracking counters for state persistence.

## 🛠️ How It Works

1. **Automated User Scraping:**
   - The bot uses `fetching_new_users.py` to automatically fetch new GitHub users based on specified criteria.
   - It leverages the GitHub API to retrieve users, removing the need for manual username lists.

2. **State Management:**
   - `state_manager.py` handles loading and saving the bot's state to `state.json`.
   - This ensures that the bot can resume from where it left off in case of interruptions.

3. **Continuous Operation:**
   - `main.py` runs an infinite loop (`while True`) to keep the bot running continuously.
   - Designed for deployment on a VM for 24/7 operation.


## 📦 Installation on local machine

### 🛠️ Prerequisites

- **🐍 Python 3.6 or higher**
- **🔑 GitHub Personal Access Token (PAT)**
  - **Scopes Required:** `read:user`, `user:follow`
  - [Creating a PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

### 📜 Steps

1. **Clone the Repository:**

    ```sh
    git https://github.com/OfficialCodeVoyage/Github_Automation_Follower_Bot.git
    cd Github_Automation_Follower_Bot
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
    requests
    python-dotenv
    ratelimit
    ```

    Then, install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

    **⚠️ Note:** Avoid installing standard library modules like `time` via `pip` as they are already included with Python.


## 📦 Installation on Virtual Machine (VM)




## 🛠️ Usage

### 1. **🔧 Configure Environment Variables**

Create a `.env` file in the root directory of the project to securely store your GitHub PAT and other configurations.

```dotenv
GITHUB_TOKEN="your_github_personal_access_token_here"
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
