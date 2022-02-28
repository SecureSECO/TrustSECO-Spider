import requests
import json

class GitHubAPICall:
    # Base URLs
    def __init__(self):
        self.base_url_repos = "https://api.github.com/repos/"
        self.base_url_users = "https://api.github.com/users/"

    # Get the information of the owner, of the repository, and of the specific version.
    def get_all_data(self, owner, repo, version, user_token):
        repository_data = self.GetData(self.base_url_repos + owner + '/' + repo, user_token)
        version_data = self.GetData(self.base_url_repos + owner + '/' + repo + '/releases/tags/' + version, user_token)
        user_data = self.GetData(self.base_url_users + owner, user_token)
        
        return (repository_data, version_data, user_data)
    
    # Perform a simple GET request, based off the given URL
    def get_data(self, api_url, user_token):
        # Basic request to get the information.
        data_response = requests.get(api_url,
                                headers={'Authorization': 'token ' + user_token, # TEMPORARY USER TOKEN FOR TESTING
                                'accept': 'application/vnd.github.v3+json'})

        # See if we got a valid response
        if data_response.status_code == 200:
            data = data_response.json()
        else:
            print('Unable to get data from GitHub')
            print('Error: ' + data_response.text)
            data = None
            
        return data
