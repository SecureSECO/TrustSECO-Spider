"""
File containing the Libraries.io API class.
This class is used to perform API calls to the Libraries.io API.
"""

import os
import time
from datetime import datetime as dt
import requests
from dotenv import load_dotenv, set_key


class LibrariesAPICall:
    def __init__(self):
        # Make sure that the .env file exists, and has the proper key-values
        if not os.path.exists('.env'):
            print('Could not find .env file')
            print('Creating new .env file')
            with open('.env', 'w') as f:
                f.write('GITHUB_TOKEN=\nLIBRARIES_TOKEN=')

        load_dotenv(dotenv_path='.env')

    def get_release_frequency(self, platform, name):
        """
        Gets the average time per release
        """

        print('Getting the average release frequency')

        # Get the first and last release dates, so we know for how long the project has been active
        latest_release_date = self.get_latest_release_date(platform, name)
        first_release_date = self.get_first_release_date(platform, name)
        # Get the release count
        release_count = self.get_release_count(platform, name)

        # Make sure that none of the required values are None
        # As we wouldn't be able to calculate the release frequency otherwise
        if latest_release_date is not None and first_release_date is not None and release_count is not None:
            latest = dt.strptime(
                latest_release_date[:-5], '%Y-%m-%dT%H:%M:%S')
            first = dt.strptime(
                first_release_date[:-5], '%Y-%m-%dT%H:%M:%S')
            # Return the average time between releases
            return (latest - first).total_seconds() / release_count
        else:
            print('Error occured while getting the average release frequency')
            return None

    def get_contributors_count(self, owner, name):
        """
        Tries to get the project's repository contributor count
        """

        print('Getting the repository contributor count')

        # Get the repository data of this project
        data = self.get_project_repository(owner, name)

        if data is not None:
            return data['github_contributions_count']
        else:
            print(
                "Error occured while getting the project's repository contributor count")
            return None

    def get_dependency_count(self, platform, name, version):
        """
        Tries to get the project's source rank
        """

        print('Getting the dependency count')

        # Get the depenency data of this project
        data = self.get_project_dependencies(platform, name, version)

        if data is not None:
            # Filter out the development dependencies, as they are not relevant for the final product
            count = 0
            for release in data['dependencies']:
                if release['kind'] != 'Development':
                    count += 1

            # Return the amount of dependencies
            return count
        else:
            print('Error occured while getting the project dependency count')
            return None

    def get_dependent_count(self, platform, name):
        """
        Tries to get the amount of dependents the project has
        """

        print('Getting the dependent count')

        data = self.get_project_information(platform, name)

        if data is not None:
            return data['dependents_count']
        else:
            print("Error occured while getting the project's dependent count")
            return None

    def get_latest_release_date(self, platform, name):
        """
        Tries to get the time of the project's latest release
        """

        print('Getting the latest release date')

        data = self.get_project_information(platform, name)

        if data is not None:
            return data['latest_release_published_at']
        else:
            print("Error occured while getting the project's latest release date")
            return None

    def get_first_release_date(self, platform, name):
        """
        Tries to get the time of the project's latest release
        """

        print('Getting the first release date')

        data = self.get_project_information(platform, name)

        if data is not None:
            return data['versions'][0]['published_at']
        else:
            print("Error occured while getting the project's first release date")
            return None

    def get_release_count(self, platform, name):
        """
        Tries to get the amount of releases the project has
        """

        print('Getting the release count')

        data = self.get_project_information(platform, name)

        if data is not None:
            return len(data['versions'])
        else:
            print("Error occured while getting the project's release count")
            return None

    def get_sourcerank(self, platform, name):
        """
        Tries to get the project's source rank
        """

        print('Getting the project source rank')

        data = self.get_project_information(platform, name)

        if data is not None:
            return data['rank']
        else:
            print("Error occured while getting the project's source rank")
            return None

    def get_project_repository(self, owner, name):
        """
        Tries to get the project repository's information from Libraries.io
        """

        # Setup the url, and perform the request
        repo_url = f'https://libraries.io/api/github/{owner}/{name}?api_key='
        data_response = self.make_api_call(repo_url)

        # If the data_response is valid, return the json data
        if data_response is not None:
            return data_response.json()
        # Else, inform the user that the request has failed, and return None
        else:
            print("Error occured while getting the project's repository information")
            return None

    def get_project_dependencies(self, platform, name, version):
        """
        Tries to get the project's dependencies from Libraries.io
        """

        # Setup the url, and perform the request
        depen_url = f'https://libraries.io/api/{platform}/{name}/{version}/dependencies?api_key='
        data_response = self.make_api_call(depen_url)

        if data_response is not None:
            return data_response.json()
        else:
            print("Error occured while getting the project's dependency information")
            return None

    def get_project_information(self, platform, name):
        """
        Tries to get the project information from Libraries.io
        """

        # Setup the url, and perform the request
        repo_url = f'https://libraries.io/api/{platform}/{name}?api_key='
        data_response = self.make_api_call(repo_url)

        # If the data_response is valid, return the json data
        if data_response is not None:
            return data_response.json()
        # Else, inform the user that the request has failed, and return None
        else:
            print("Error occured while getting the project information")
            return None

    def make_api_call(self, api_url):
        """
        Perform a simple GET request, based off the given URL

        If successful, returns the response
        If not, returns None
        """

        # See if the user's Libraries.io token is known
        # If not, authenticate the user
        if os.getenv('LIBRARIES_TOKEN') is None or os.getenv('LIBRARIES_TOKEN') == '':
            print('No Libraries.io token found.')
            print('Please enter your token:')

            token = input()

            # See if the user entered a valid token
            # by making sure text has been entered
            # and that the entered text is alphanumeric
            if len(token) > 0 and token.isalnum():
                print('Received API token')
                """We should probably test this token via some kind of quick api call"""

                # Write the token to the .env file
                set_key('.env', 'LIBRARIES_TOKEN', token)

                # Reload the environment variables
                # As otherwise the environmental tokens would not have been updated
                load_dotenv(dotenv_path='.env', override=True)
            # If not, stop the program
            else:
                print('Authentication failed.')
                """Perhaps a retry would be better here?"""
                return None

        # Catch any requests errors
        try:
            # Basic request to get the information.
            data_response = requests.get(
                api_url + os.getenv('LIBRARIES_TOKEN'))
        except requests.exceptions.RequestException as error:
            print('Requests encountered an error:')
            print(error)
            return None

        # See if we got a valid response
        if data_response.status_code == 200:
            return data_response
        # See if we got a rate limit error
        elif data_response.status_code == 429:
            # See if the header includes the rate limit reset time
            # If so, use it
            if 'Retry-After' in data_response.headers:
                retry_time = data_response.headers['Retry-After']
                print(
                    f'Too many requests. Trying again in {retry_time} seconds.')
                time.sleep(retry_time)
                return self.make_api_call(api_url)
            # If not, use 30 seconds, as it is half the rate limit reset time
            else:
                print('Too many requests. Trying again in 30 seconds.')
                time.sleep(30)
                return self.make_api_call(api_url)
        else:
            print('Unable to get data from Libraries.io')
            print(f'Error: {data_response.status_code}')
            return None
