"""
Basic demo file, purely for demonstration purposes.

Allows the user to test the Device Flow authentication process,
GitHub API calls, and spidering.
"""
# For getting additional arguments from the command line
import sys
# For pretty printing the JSON data
import json
# For accessing the GitHub data-points
from controller import get_data


def numpy_demo():
    """
    Function containing the code for the numpy demo.

    First, we set the input JSON to include numpy's details,
    and then we set the wanted data-points.
    """

    # Set the input JSON
    input_json = {
        "project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
            "project_year": 2021
        },
        "gh_data_points": [
            "gh_contributor_count",
            "gh_user_count",
            "gh_total_download_count",
            "gh_release_download_count",
            "gh_yearly_commit_count",
            "gh_given_year_commit_count",
            "gh_repository_language",
            "gh_open_issues_count",
            "gh_zero_response_issues_count",
            "gh_issue_ratio",
            "gh_average_resolution_time",
            "gh_owner_stargazer_count"
        ],
        "lib_data_points": [
            "lib_release_frequency",
            "lib_contributor_count",
            "lib_dependency_count",
            "lib_dependent_count",
            "lib_latest_release_date",
            "lib_first_release_date",
            "lib_release_count",
            "lib_sourcerank"
        ],
        "cve_data_points": [
            "cve_count",
            "cve_vulnerabilities",
            "cve_codes"
        ]
    }

    # Get the data
    print(json.dumps(get_data(input_json), indent=4))


def afnetworking_demo():
    """
    Function containing the code for the AFNetworking demo.

    First, we set the input JSON to include AFNetworking's details,
    and then we set the wanted data-points.
    """

    # Set the input JSON
    input_json = {
        "project_info": {
            "project_platform": "CocoaPods",
            "project_owner": "AFNetworking",
            "project_name": "AFNetworking",
            "project_release": "4.0.0",
            "project_year": 2019
        },
        "gh_data_points": [
            "gh_contributor_count",
            "gh_user_count",
            "gh_total_download_count",
            "gh_release_download_count",
            "gh_yearly_commit_count",
            "gh_given_year_commit_count",
            "gh_repository_language",
            "gh_open_issues_count",
            "gh_zero_response_issues_count",
            "gh_issue_ratio",
            "gh_average_resolution_time",
            "gh_owner_stargazer_count"
        ],
        "lib_data_points": [
            "lib_release_frequency",
            "lib_contributor_count",
            "lib_dependency_count",
            "lib_dependent_count",
            "lib_latest_release_date",
            "lib_first_release_date",
            "lib_release_count",
            "lib_sourcerank"
        ],
        "cve_data_points": [
            "cve_count",
            "cve_vulnerabilities",
            "cve_codes"
        ]
    }

    # Get the data
    print(json.dumps(get_data(input_json), indent=4))


if __name__ == '__main__':
    # See if the user passed arguments
    if len(sys.argv) > 1:
        # If numpy is specified, run the numpy demo
        if 'numpy' in sys.argv:
            numpy_demo()

        # If cocoapods is specified, run the cocoapods demo
        if 'afnetworking' in sys.argv:
            afnetworking_demo()

        # If all is specified, run both demos
        if 'all' in sys.argv:
            numpy_demo()
            afnetworking_demo()
    else:
        print('No arguments passed.')
        print('Please specify which library you would like to gather data of:')
        print('\t- numpy')
        print('\t- afnetworking')
        print('\t- all')
