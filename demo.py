"""Basic demo file, purely for demonstration purposes.

Before running this file, the Flask application needs to be started. (instructions for which can be found in the README.md file)
"""
# Import for getting input parameters
import sys
# Import for pretty printing the JSON data
import json
# Import for sending and handling HTTP requests
import requests
# Import the ClamAV scanner
from src.clamav.clamav_scanner import ClamAVScanner


def numpy_demo(scan_viruses: bool) -> None:
    """
    Function containing the code for the numpy demo.

    Parameters:
        scan_virusses (bool): Boolean denoting if we also want to scan for viruses
    """

    # Set the input JSON
    input_json = {
        "project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
        },
        "gh_data_points": [
            "gh_contributor_count",
            "gh_user_count",
            "gh_total_download_count",
            "gh_release_download_count",
            "gh_yearly_commit_count",
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
        ],
        "so_data_points": [
            "so_popularity"
        ]
    }

    # If the user wants to scan for viruses, add the virus scanning data-points
    if scan_viruses:
        input_json["virus_scanning"] = ["virus_ratio"]

    # Get the data
    response = requests.post('http://localhost:5000/get_data',
                             headers={'Content-type': 'application/json'}, json=input_json)

    # Get the data
    print(json.dumps(response.json(), indent=4))


def afnetworking_demo(scan_viruses: bool) -> None:
    """
    Function containing the code for the AFNetworking demo.

    Parameters:
        scan_virusses (bool): Boolean denoting if we also want to scan for viruses
    """

    # Set the input JSON
    input_json = {
        "project_info": {
            "project_platform": "CocoaPods",
            "project_owner": "AFNetworking",
            "project_name": "AFNetworking",
            "project_release": "4.0.0",
        },
        "gh_data_points": [
            "gh_contributor_count",
            "gh_user_count",
            "gh_total_download_count",
            "gh_release_download_count",
            "gh_yearly_commit_count",
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
        ],
        "so_data_points": [
            "so_popularity"
        ]
    }

    # If the user wants to scan for viruses, add the virus scanning data-points
    if scan_viruses:
        input_json["virus_scanning"] = ["virus_ratio"]

    # Get the data
    response = requests.post('http://localhost:5000/get_data',
                             headers={'Content-type': 'application/json'}, json=input_json)

    # Get the data
    print(json.dumps(response.json(), indent=4))


def virus_free_demo() -> None:
    """
    Function containing the code for the safe virus-scan demo.
    """

    sc = ClamAVScanner()

    ratio = sc.get_virus_ratio([
        'https://github.com/numpy/numpy/releases/download/v1.22.4/1.22.4-changelog.rst',
        'https://github.com/numpy/numpy/releases/download/v1.22.4/numpy-1.22.4.tar.gz',
        'https://github.com/numpy/numpy/releases/download/v1.22.4/numpy-1.22.4.zip',
        'https://github.com/numpy/numpy/releases/download/v1.22.4/README.rst',
        'https://github.com/numpy/numpy/archive/refs/tags/v1.22.4.zip',
        'https://github.com/numpy/numpy/archive/refs/tags/v1.22.4.tar.gz'
    ])

    print(f'Virus ratio: {ratio}')


def virus_infected_demo() -> None:
    """
    Function containing the code for the infected virus-scan demo.
    """

    sc = ClamAVScanner()

    ratio = sc.get_virus_ratio([
        'https://github.com/fire1ce/eicar-standard-antivirus-test-files/archive/refs/heads/master.zip'
    ])

    print(f'Virus ratio: {ratio}')


if __name__ == '__main__':
    # See if the user passed arguments
    if len(sys.argv) > 1:
        # See if we also want to run the virus scanner
        scan_viruses = False
        if 'virus' in sys.argv:
            scan_viruses = True

        # If numpy is specified, run the numpy demo
        if 'numpy' in sys.argv:
            numpy_demo(scan_viruses)

        # If afnetworking is specified, run the afnetworking demo
        if 'afnetworking' in sys.argv:
            afnetworking_demo(scan_viruses)

        # If virus_s is specified, run the safe virus demo
        if 'virus_s' in sys.argv:
            virus_free_demo()

        # If virus_i is specified, run the infected virus demo
        if 'virus_i' in sys.argv:
            virus_infected_demo()

        # If all is specified, run both demos
        if 'all' in sys.argv:
            numpy_demo(scan_viruses)
            afnetworking_demo(scan_viruses)
    else:
        print('No arguments passed.')
        print('Please specify which library you would like to gather data of:')
        print('\t- numpy')
        print('\t- afnetworking')
        print('\t- virus_s (safe)')
        print('\t- virus_i (infected)')
        print('\t- all')
        print('If you would like to run the virus scanner, add the \'virus\' argument and make sure the virus scanner is also running.')


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
