"""
Basic main file, purely for demonstration purposes.
"""

import os
import json
from dotenv import load_dotenv
from GitHub.github_api_calls import GitHubAPICall
from GitHub.github_get_token import authenticate_user

load_dotenv()

# This file currently only contains a basic script in order to show off the current functionality
g = GitHubAPICall()

if os.getenv('GITHUB_TOKEN') is None:
    print("No GitHub token found. Authenticating user...")

    # Authenticate the user
    authenticate_user('1c3bf96ae6a2ec75435c')
else:
    print("GitHub token found. Getting data...")

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
