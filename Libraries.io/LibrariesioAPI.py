import requests

class LibrariesioAPICall:
    
    def __init__(self):
        self.api_key = input("Please enter your Libraries.io API key: ")
    
    # Get information about a package and its versions
    # For example, platform: NPM, name: base62, api_key: API key of the user
    def get_package_and_version_information(self, platform, name, api_key):
        data_response = requests.get('https://libraries.io/api/' + str(platform) + '/' + str(name) + '?api_key=' + str(api_key))
        print(data_response.json())
    
    # Get a list of dependencies for a version of a project, pass latest to get dependency info for the latest available version
    # For example, platform: NPM, name: base62, version: 2.0.1 (or latest), api_key: API key of the user
    def get_dependencies_project(self, platform, name, version, api_key):
        data_response = requests.get('https://libraries.io/api/' + str(platform) + '/' + str(name) + '/' + str(version) + '/dependencies?api_key=' + str(api_key))
        print(data_response.json())
    
    # Get breakdown of SourceRank score for a given project
    def get_project_sourcerank(self, platform, name, api_key):
        data_response = requests.get('https://libraries.io/api/' + str(platform) + '/' + str(name) + '/sourcerank?api_key=' + str(api_key))
        print(data_response.json())