# GitHub Follow by Username

## Introduction
`GitHub Follow by Username` is a Python script that allows you to follow GitHub users by their usernames from a list in a file. This tool is particularly useful for managing your followings on GitHub efficiently.

## Features
- Follow any GitHub user by their username.
- Specify the starting line to continue following users from a specific point.
- Handles GitHub rate limits with a delay between follow actions.

## Installation
### Prerequisites
- Python 3.6 or higher
- GitHub personal access token

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/OfficialCodeVoyage/GitHub_follow_by_username.git
    cd GitHub_follow_by_username
    ```

2. Install the required Python packages:
    ```sh
    pip install requests
    pip install time
    ```

## Usage
1. Create a file named `usernames.txt` in the same directory as the script and add the GitHub usernames you want to follow, one per line.

2. Run the script with your GitHub personal access token and specify the line number to start from (0-indexed). Replace `'your_github_personal_access_token'` with your actual GitHub personal access token and set the `START_LINE` as needed:

    ```python
    if __name__ == "__main__":
        FILE_PATH = 'usernames.txt'  # Path to the usernames file
        TOKEN = 'your_github_personal_access_token'  # Your GitHub personal access token
        START_LINE = 0  # The line number to start from (0-indexed)

        main(FILE_PATH, TOKEN, START_LINE)
    ```

### Script Details
- **read_usernames(file_path)**: Reads usernames from a specified file and returns them as a list.
- **follow_user(username, headers)**: Sends a PUT request to the GitHub API to follow a user.
- **main(file_path, token, start_line)**: Reads the usernames from the file and follows users starting from the specified line. It handles rate limits by adding a delay between follow actions.

## Contributing
We welcome contributions from the community! Here’s how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
