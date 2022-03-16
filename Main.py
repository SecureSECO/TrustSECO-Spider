from GitHub.GitHubAPICall import GitHubAPICall
from GitHub.GitHubToken import authenticate_user
import json

# This file currently only contains a basic script in order to show off the current functionality
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
    2021, 
    # User gitHub token
    authenticate_user(
        # Temporary testing client-id
        '1c3bf96ae6a2ec75435c'
        )
    )

# Print the json data in a readable way
print(json.dumps(all_data, indent=4))