"""
File containing the class that handles all the input and output of the program.

This file will be the file that is run by the Node.JS program.
"""

# Import needed libraries
import os
import json
from dotenv import set_key
import constants
# Import the data-getting modules
from GitHub.github_api_calls import GitHubAPICall
from GitHub.github_spider import GitHubSpider
from LibrariesIO.libaries_io_api_calls import LibrariesAPICall


class Controller:
    """
    Class to facilitate input from, and output to, the Node.JS program.

    It will try and get input from the console in form of a JSON string.
    It will then go through this JSON object to find the required information, and the wanted data-points.
    These data-points will then be requested from the actual API classes,
    and then returned to the Node.JS program by placing a JSON string on the console
    """

    def __init__(self) -> None:
        # API objects
        self.gh_api = GitHubAPICall()
        self.lib_api = LibrariesAPICall()

        # Spider objects
        self.gh_spider = GitHubSpider()

    def run(self, input_json):
        """
        This is the main looping function of the program.

        It will try to read the console to see if a new command has been recieved.
        """

        # Retrieve the project information
        platform = input_json["project_info"]["project_platform"]
        owner = input_json["project_info"]["project_owner"]
        repo_name = input_json["project_info"]["project_name"]
        release = input_json["project_info"]["project_release"]
        year = input_json["project_info"]["project_year"]

        # Create an output JSON object
        output_json = {}

        # Request the data from GitHub
        output_json.update({'gh_data_points': self.get_github_data(
            owner, repo_name, release, year, input_json["gh_data_points"])})

        # Libraries.io does not use 'v' in their version numbers, so we need to remove it if it is there
        if release[0].lower() == 'v':
            lib_release = release[1:]
        else:
            lib_release = release

        # Request the data from Libraries.io
        output_json.update({'lib_data_points': self.get_libraries_data(
            platform, owner, repo_name, lib_release, input_json["lib_data_points"])})

        # Print the output JSON object to the console
        print(json.dumps(output_json))

    def get_github_data(self, owner, repo_name, release, year, wanted_data):
        """
        This function will get the data from GitHub.

        It will then return a JSON string containing the data.
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
            elif data_point == "gh_given_year_commit_count":
                return_data.update(
                    {data_point: self.gh_api.get_commit_count_in_year(owner, repo_name, year)})
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

    def get_libraries_data(self, platform, owner, repo_name, release, wanted_data):
        """
        This function will get the data from Libraries.io.

        It will then return a JSON string containing the data.
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


def get_data(input_json):
    """
    This function will start the controller.
    """

    # Create a new controller
    controller = Controller()

    # Start the controller
    controller.run(input_json)


def update_tokens(github_token, libraries_token):
    """
    This function will update the environmental variable with the given GitHub and Libraries.io tokens
    """

    # Make sure the .env file exists
    if not os.path.exists(constants.ENVIRON_FILE):
        with open(constants.ENVIRON_FILE, 'w') as f:
            f.write(f'{constants.GITHUB_TOKEN}=\n{constants.LIBRARIES_TOKEN}=')

    # Update the .env file
    set_key(constants.ENVIRON_FILE, constants.GITHUB_TOKEN, github_token)
    set_key(constants.ENVIRON_FILE, constants.LIBRARIES_TOKEN, libraries_token)
