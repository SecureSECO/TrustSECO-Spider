"""File containing the Controller of the TrustSECO-Spider


This file contains the Controller class, which contains the logic used to run the spider.
It also contains some static methods that an outside program/end-user can use to get data from the TrustSECO-Spider.

    Typical usage:

    foo = get_data('input_json')
"""

# Import needed libraries
import os
from dotenv import set_key
import constants
# Import the data-getting modules
# API calls
from src.api_calls.github_api_calls import GitHubAPICall
from src.api_calls.libaries_io_api_calls import LibrariesAPICall
# Spiders
from src.spiders.github_spider import GitHubSpider
from src.spiders.cve_spider import CVESpider
from src.spiders.stackoverflow_spider import StackOverflowSpider


class Controller:
    """Class methods for controlling the TrustSECO-Spider

    This class receives an JSON object as input, and will return an JSON object as output.
    The output JSON object will contain the data as requested by the input JSON object.

    Attributes:
        gh_api (GitHubAPICall): The GitHub API object
        lib_api (LibrariesAPICall): The Libraries.IO API object
        gh_spider (GitHubSpider): The GitHub spider object
        cve_spider (CVESpider): The CVE spider object
        so_spider (StackOverflowSpider): The StackOverflow spider object
    """

    def __init__(self):
        """Initializes the Controller object by setting the data-gathering objects."""
        # API objects
        self.gh_api = GitHubAPICall()
        self.lib_api = LibrariesAPICall()

        # Spider objects
        self.gh_spider = GitHubSpider()
        self.cve_spider = CVESpider()
        self.so_spider = StackOverflowSpider()

    def run(self, input_json) -> dict:
        """
        This is the main looping function of the program.

        It will try to read the console to see if a new command has been received.

        Parameters:
            input_json (dict): The input JSON object

            This input JSON object contains information about which package is to be spidered,
            and what data is to be returned.

        Returns:
            dict: The output JSON object

            This output JSON object contains the data as requested by the input JSON object.
        """

        # Make sure we got the information we need
        if 'project_info' not in input_json:
            print('Error: no project information found')
            return {'Error': 'Error: no project information found'}

        # Make sure all of the wanted project information is available
        if 'project_platform' and 'project_owner' and 'project_name' and 'project_release' in input_json["project_info"]:
            # Retrieve the project information
            platform = input_json["project_info"]["project_platform"]
            owner = input_json["project_info"]["project_owner"]
            repo_name = input_json["project_info"]["project_name"]
            release = input_json["project_info"]["project_release"]

            # Create an output JSON object
            output_json = {}

            # Request the data from GitHub
            if 'gh_data_points' in input_json:
                # Tell the user what is going on
                print('-------------------')
                print('Getting GitHub data...')

                # Actually request the data
                output_json.update({'gh_data_points': self.get_github_data(
                    owner, repo_name, release, input_json["gh_data_points"])})

            # Request the data from Libraries.IO
            if 'lib_data_points' in input_json:
                # Tell the user what is going on
                print('-------------------')
                print('Getting Libraries.IO data...')

                # Libraries.io does not use 'v' in their version numbers, so we need to remove it if it is there
                if release[0].lower() == 'v':
                    lib_release = release[1:]
                else:
                    lib_release = release

                # Actually request the data
                output_json.update({'lib_data_points': self.get_libraries_data(
                    platform, owner, repo_name, lib_release, input_json["lib_data_points"])})

            # Request the data from the CVE website
            if 'cve_data_points' in input_json:
                # Tell the user what is going on
                print('-------------------')
                print('Getting CVE data...')

                # Actually request the data
                output_json.update({'cve_data_points': self.get_cve_data(
                    repo_name, input_json["cve_data_points"])})

            # Request the data from the StackOverflow website
            if 'so_data_points' in input_json:
                # Tell the user what is going on
                print('-------------------')
                print('Getting StackOverflow data...')

                # Actually request the data
                output_json.update({'so_data_points': self.get_so_data(
                    repo_name, input_json["so_data_points"])})

            print('-------------------')

            # Print the output JSON object to the console
            return output_json
        else:
            print('Error: missing project information')
            return 'Error: missing project information'

    def get_github_data(self, owner, repo_name, release, wanted_data) -> dict:
        """
        Get the data from GitHub.

        Parameters:
            owner (str): The owner of the repository
            repo_name (str): The name of the repository
            release (str): The release name
            year (str): The year
            wanted_data (list): The list of data points to be returned

        Returns:
            dict: The requested GitHub data
        """

        # Create a JSON object to store the data
        return_data = {}

        # Loop through the wanted data list and retrieve the data
        for data_point in wanted_data:
            if data_point == "gh_contributor_count":
                return_data.update(
                    {data_point: self.gh_api.get_repository_contributor_count(owner, repo_name)})
            elif data_point == "gh_user_count":
                return_data.update(
                    {data_point: self.gh_spider.get_repository_user_count(owner, repo_name)})
            elif data_point == "gh_total_download_count":
                return_data.update(
                    {data_point: self.gh_api.get_total_download_count(owner, repo_name)})
            elif data_point == "gh_release_download_count":
                return_data.update(
                    {data_point: self.gh_api.get_release_download_count(owner, repo_name, release)})
            elif data_point == "gh_yearly_commit_count":
                return_data.update(
                    {data_point: self.gh_api.get_yearly_commit_count(owner, repo_name)})
            elif data_point == "gh_repository_language":
                return_data.update(
                    {data_point: self.gh_api.get_repository_language(owner, repo_name)})
            elif data_point == "gh_gitstar_ranking":
                return_data.update(
                    {data_point: self.gh_api.get_gitstar_ranking(owner, repo_name)})
            elif data_point == "gh_open_issues_count":
                return_data.update(
                    {data_point: self.gh_spider.get_repository_open_issue_count(owner, repo_name)})
            elif data_point == "gh_zero_response_issues_count":
                return_data.update(
                    {data_point: self.gh_api.get_zero_responses_issue_count(owner, repo_name)})
            elif data_point == "gh_release_issues_count":
                return_data.update(
                    {data_point: self.gh_api.issue_count_per_release(owner, repo_name, release)})
            elif data_point == "gh_issue_ratio":
                return_data.update(
                    {data_point: self.gh_spider.get_repository_issue_ratio(owner, repo_name)})
            elif data_point == "gh_average_resolution_time":
                return_data.update(
                    {data_point: self.gh_api.get_average_issue_resolution_time(owner, repo_name)})
            elif data_point == "gh_owner_stargazer_count":
                return_data.update(
                    {data_point: self.gh_api.get_owner_stargazer_count(owner)})
            else:
                print(f"Error: invalid data point {data_point}")
                return_data.update({data_point: None})

        # Return the requested data-points
        return return_data

    def get_libraries_data(self, platform, owner, repo_name, release, wanted_data) -> dict:
        """
        Get the data from Libraries.IO.

        Parameters:
            platform (str): The platform of the repository
            owner (str): The owner of the repository
            repo_name (str): The name of the repository
            release (str): The release name
            wanted_data (list): The list of data points to be returned

        Returns:
            dict: The requested Libraries.IO data
        """

        # Create a JSON object to store the data
        return_data = {}

        # Loop through the wanted data list and retrieve the data
        for data_point in wanted_data:
            if data_point == "lib_release_frequency":
                return_data.update(
                    {data_point: self.lib_api.get_release_frequency(platform, repo_name)})
            elif data_point == "lib_contributor_count":
                return_data.update(
                    {data_point: self.lib_api.get_contributors_count(owner, repo_name)})
            elif data_point == "lib_dependency_count":
                return_data.update(
                    {data_point: self.lib_api.get_dependency_count(platform, repo_name, release)})
            elif data_point == "lib_dependent_count":
                return_data.update(
                    {data_point: self.lib_api.get_dependent_count(platform, repo_name)})
            elif data_point == "lib_latest_release_date":
                return_data.update(
                    {data_point: self.lib_api.get_latest_release_date(platform, repo_name)})
            elif data_point == "lib_first_release_date":
                return_data.update(
                    {data_point: self.lib_api.get_first_release_date(platform, repo_name)})
            elif data_point == "lib_release_count":
                return_data.update(
                    {data_point: self.lib_api.get_release_count(platform, repo_name)})
            elif data_point == "lib_sourcerank":
                return_data.update(
                    {data_point: self.lib_api.get_sourcerank(platform, repo_name)})
            else:
                print(f"Error: invalid data point {data_point}")
                return_data.update({data_point: None})

        # Return the requested data-points
        return return_data

    def get_cve_data(self, repo_name, wanted_data) -> dict:
        """
        Get the data from CVE website.

        Parameters:
            repo_name (str): The name of the repository
            wanted_data (list): The list of data points to be returned

        Returns:
            dict: The requested CVE data
        """

        # Create a JSON object to store the data
        return_data = {}

        for data_point in wanted_data:
            if data_point == "cve_count":
                return_data.update(
                    {data_point: self.cve_spider.get_cve_vulnerability_count(repo_name)})
            elif data_point == "cve_vulnerabilities":
                return_data.update(
                    {data_point: self.cve_spider.get_all_cve_data(repo_name)})
            elif data_point == "cve_codes":
                return_data.update(
                    {data_point: self.cve_spider.get_cve_codes(repo_name)})
            else:
                print(f"Error: invalid data point {data_point}")
                return_data.update({data_point: None})

        # Return the requested data-points
        return return_data

    def get_so_data(self, repo_name, wanted_data) -> dict:
        """
        Get the data from Stack Overflow.

        Parameters:
            repo_name (str): The name of the repository
            wanted_data (list): The list of data points to be returned

        Returns:
            dict: The requested Stack Overflow data
        """

        # Create a JSON object to store the data
        return_data = {}

        for data_point in wanted_data:
            if data_point == "so_popularity":
                return_data.update(
                    {data_point: self.so_spider.get_monthly_popularity(repo_name)})
            else:
                print(f"Error: invalid data point {data_point}")
                return_data.update({data_point: None})

        # Return the requested data-points
        return return_data


def get_data(input_json):
    """
    This function will start the controller.
    """

    # Create a new controller
    controller = Controller()

    # Start the controller
    return controller.run(input_json)


def update_token_gh(github_token):
    """
    This function will update the environmental variables with the given GitHub token
    """

    # Make sure the .env file exists
    if not os.path.exists(constants.ENVIRON_FILE):
        with open(constants.ENVIRON_FILE, 'w') as f:
            f.write(f'{constants.GITHUB_TOKEN}=\n{constants.LIBRARIES_TOKEN}=')

    # Update the .env file
    set_key(constants.ENVIRON_FILE, constants.GITHUB_TOKEN, github_token)


def update_token_lib(libraries_token):
    """
    This function will update the environmental variable with the given Libraries.io token
    """

    # Make sure the .env file exists
    if not os.path.exists(constants.ENVIRON_FILE):
        with open(constants.ENVIRON_FILE, 'w') as f:
            f.write(f'{constants.GITHUB_TOKEN}=\n{constants.LIBRARIES_TOKEN}=')

    # Update the .env file
    set_key(constants.ENVIRON_FILE, constants.LIBRARIES_TOKEN, libraries_token)


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
