import requests
from bs4 import BeautifulSoup

# The URL of the Gist page
url = "https://gist.github.com/paulmillr/2657075/a31455729440672467ada20ac10452d74a871e54"

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table that contains the usernames
    table = soup.find('table')

    if table:
        # Extract usernames from the table rows
        usernames = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            username_cell = row.find('td')
            if username_cell:
                # Extract the text and strip unnecessary characters
                username_with_name = username_cell.text.strip()

                # Split the username at the first occurrence of '(' and take the first part
                username = username_with_name.split('(')[0].strip()

                # Append the cleaned username to the list
                usernames.append(username)

        # Print the usernames
        for username in usernames:
            print(username)
    else:
        print("Table not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
