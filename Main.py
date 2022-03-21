"""
Basic main file, purely for demonstration purposes.
"""

import os
import os.path
import json
from dotenv import load_dotenv
from GitHub.github_api_calls import GitHubAPICall
from GitHub.github_get_token import authenticate_user

# Make sure that the .env file exists
if not os.path.exists('.env'):
    with open('.env', 'wt', encoding='utf-8') as env_file:
        pass

# Load the .env file
load_dotenv()

# Authenticate the user if needed
if os.getenv('GITHUB_TOKEN') is None:
    print("No GitHub token found. Authenticating user...")

    # Authenticate the user
    authenticate_user('1c3bf96ae6a2ec75435c')
else:
    print("GitHub token found. Getting data...")

# Create an API call object
g = GitHubAPICall()

# Get the data
all_data = g.get_all_data(
    # Owner
    'numpy',
    # Repository
    'numpy',
    # Version
    'v1.22.3',
    # Commit year
    2021
    )

# Print the json data in a readable way
print(json.dumps(all_data, indent=4))
