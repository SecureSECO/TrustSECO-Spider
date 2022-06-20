"""File containing the unit tests for the controller module."""

# Imports for testing
import pytest
from unittest import mock
# Import the Controller class
from controller import Controller


class TestControllerRun:
    """Class containing the unit tests for the controller module."""

    def test_run_no_proj_info(self) -> None:
        """
        Test for when the project information is missing from the input JSON.
        """
        # make an input JSON with no project information
        input_json = {}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Check that the response is correct
        assert result == {'Error': 'Error: no project information found'}

    @pytest.mark.parametrize('input_json, return_value', [
        (
            {"project_info": {
                "project_owner": 'numpy',
                "project_name": 'numpy',
                "project_release": 'v1.22.1'}},
            {'Error': 'missing project information (project_platform)'}
        ),
        (
            {"project_info": {
                "project_platform": 'Pypi',
                "project_name": 'numpy',
                "project_release": 'v1.22.1'}},
            {'Error': 'missing project information (project_owner)'}
        ),
        (
            {"project_info": {
                "project_platform": 'Pypi',
                "project_owner": 'numpy',
                "project_release": 'v1.22.1'}},
            {'Error': 'missing project information (project_name)'}
        ),
        (
            {"project_info": {
                "project_platform": 'Pypi',
                "project_owner": 'numpy',
                "project_name": 'numpy'}},
            {'Error': 'missing project information (project_release)'}
        )
    ])
    def test_run_missing_info(self, input_json: dict, return_value: dict) -> None:
        """
        Test for when a required field within the project information is missing from the input JSON.

        Parameters:
            input_json (dict): The input json to run the controller with
        """

        # Run the controller with the input JSON
        response_data = Controller().run(input_json)

        # Assert that the returned error is equal to the defined error in the controller
        assert response_data == return_value

    @mock.patch('controller.Controller.get_github_data', new=mock.Mock(return_value={"gh": "mock"}))
    def test_run_gh(self) -> None:
        """
        Test for when we only request GitHub data.
        """

        # make an input JSON with only requesting GitHub data
        input_json = {
            "project_info": {
                "project_platform": "Pypi",
                "project_owner": "numpy",
                "project_name": "numpy",
                "project_release": "v1.22.1"
            },
            "gh_data_points": []
        }

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the Github data
        # and that the value is equal to the one we specified
        assert result == {"gh": "mock"}

    @mock.patch('controller.Controller.get_libraries_data', new=mock.Mock(return_value={"lb": "mock"}))
    def test_run_lib(self) -> None:
        """
        Test for when we only request Libraries.io data.
        """

        # make an input JSON with only requesting Libraries.io data
        input_json = {
            "project_info": {
                "project_platform": "Pypi",
                "project_owner": "numpy",
                "project_name": "numpy",
                "project_release": "v1.22.1"
            },
            "lib_data_points": []
        }

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the Libraries.io data
        # and that the value is equal to the one we specified
        assert result == {"lb": "mock"}

    @mock.patch('controller.Controller.get_cve_data', new=mock.Mock(return_value={"cve": "mock"}))
    def test_run_cve(self) -> None:
        """
        Test for when we only request CVE data.
        """

        # make an input JSON with only requesting CVE data
        input_json = {
            "project_info": {
                "project_platform": "Pypi",
                "project_owner": "numpy",
                "project_name": "numpy",
                "project_release": "v1.22.1"
            },
            "cve_data_points": []
        }

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the CVE data
        # and that the value is equal to the one we specified
        assert result == {"cve": "mock"}

    @mock.patch('controller.Controller.get_so_data', new=mock.Mock(return_value={"so": "mock"}))
    def test_run_so(self) -> None:
        """
        Test for when we only request Stack Overflow data.
        """

        # make an input JSON with only requesting Stack Overflow data
        input_json = {
            "project_info": {
                "project_platform": "Pypi",
                "project_owner": "numpy",
                "project_name": "numpy",
                "project_release": "v1.22.1",
            },
            "so_data_points": []
        }

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the Stack Overflow data
        # and that the value is equal to the one we specified
        assert result == {"so": "mock"}

    @mock.patch('controller.Controller.get_virus_data', new=mock.Mock(return_value={"virus": "mock"}))
    def test_run_virus(self) -> None:
        """
        Test for when we only request virus scan data.
        """

        # make an input JSON with only requesting virus scan data
        input_json = {
            "project_info": {
                "project_platform": "Pypi",
                "project_owner": "numpy",
                "project_name": "numpy",
                "project_release": "v1.22.1"
            },
            "virus_scanning": []
        }

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the virus scan data
        # and that the value is equal to the one we specified
        assert result == {"virus": "mock"}


class TestControllerData:

    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_repository_contributor_count')
    @mock.patch('src.github.github_spider.GitHubSpider.get_repository_user_count')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_total_download_count')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_release_download_count')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_yearly_commit_count')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_repository_language')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_gitstar_ranking')
    @mock.patch('src.github.github_spider.GitHubSpider.get_repository_open_issue_count')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_zero_responses_issue_count')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.issue_count_per_release')
    @mock.patch('src.github.github_spider.GitHubSpider.get_repository_issue_ratio')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_average_issue_resolution_time')
    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_owner_stargazer_count')
    def test_get_github_data(self, mock_owner_stargazer_count: mock.Mock, mock_average_issue_resolution_time: mock.Mock, mock_repo_issue_ratio: mock.Mock,
                             mock_issue_count_per_release: mock.Mock, mock_zero_responses_issue_count: mock.Mock, mock_repo_open_issue_count: mock.Mock,
                             mock_gitstar_ranking: mock.Mock, mock_repo_language: mock.Mock, mock_yearly_commit_count: mock.Mock,
                             mock_release_download_count: mock.Mock, mock_total_download_count: mock.Mock, mock_repo_user_count: mock.Mock,
                             mock_repo_contributor_count: mock.Mock) -> None:
        """
        Test for when we only request Github data.
        """

        # Set the required inputs
        owner = "numpy"
        repo_name = "numpy"
        release = "v1.22.1"
        wanted_data = ["gh_contributor_count", "gh_user_count", "gh_total_download_count",
                       "gh_release_download_count", "gh_yearly_commit_count", "gh_repository_language",
                       "gh_gitstar_ranking", "gh_open_issues_count", "gh_zero_response_issues_count",
                       "gh_release_issues_count", "gh_issue_ratio", "gh_average_resolution_time",
                       "gh_owner_stargazer_count", "unknown"]

        # Set the mock return values for the functions we are testing
        mock_repo_contributor_count.return_value = 3
        mock_repo_user_count.return_value = 20
        mock_total_download_count.return_value = 23
        mock_release_download_count.return_value = 11
        mock_yearly_commit_count.return_value = 50
        mock_repo_language.return_value = "python"
        mock_gitstar_ranking.return_value = 4
        mock_repo_open_issue_count.return_value = 3
        mock_zero_responses_issue_count.return_value = 2
        mock_issue_count_per_release.return_value = 5
        mock_repo_issue_ratio.return_value = 0.6
        mock_average_issue_resolution_time.return_value = 300
        mock_owner_stargazer_count.return_value = 2

        # Run the controller with the input JSON
        result = Controller().get_github_data(owner, repo_name, release, wanted_data)

        # Assert that the returned dictionary only contains the Github data
        # and that the value is equal to the one we specified
        assert result == {"gh_contributor_count": 3, "gh_user_count": 20, "gh_total_download_count": 23,
                          "gh_release_download_count": 11, "gh_yearly_commit_count": 50, "gh_repository_language": "python",
                          "gh_gitstar_ranking": 4, "gh_open_issues_count": 3, "gh_zero_response_issues_count": 2,
                          "gh_release_issues_count": 5, "gh_issue_ratio": 0.6, "gh_average_resolution_time": 300,
                          "gh_owner_stargazer_count": 2, "unknown": None}

    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_release_frequency')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_contributors_count')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_dependency_count')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_dependent_count')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_latest_release_date')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_first_release_date')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_release_count')
    @mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_sourcerank')
    def test_get_libraries_data(self, mock_sourcerank: mock.Mock, mock_release_count: mock.Mock, mock_first_release_date: mock.Mock,
                                mock_latest_release_date: mock.Mock, mock_dependent_count: mock.Mock, mock_dependency_count: mock.Mock,
                                mock_contributors_count: mock.Mock, mock_release_frequency: mock.Mock) -> None:
        """
        Test for the get_libraries_data function.
        """

        # Set the required inputs
        platform = "Pypi"
        owner = "numpy"
        repo_name = "numpy"
        release = "v1.22.1"
        wanted_data = ["lib_release_frequency", "lib_contributor_count", "lib_dependency_count", "lib_dependent_count",
                       "lib_latest_release_date", "lib_first_release_date", "lib_release_count", "lib_sourcerank", "unknown"]

        # Set the mock return values for the functions we are testing
        mock_release_frequency.return_value = 1
        mock_contributors_count.return_value = 5
        mock_dependency_count.return_value = 3
        mock_dependent_count.return_value = 2
        mock_latest_release_date.return_value = "2016-04-20T04:09:15.000Z"
        mock_first_release_date.return_value = "2016-04-19T04:09:15.000Z"
        mock_release_count.return_value = 2
        mock_sourcerank.return_value = 5

        # Run the function we are testing
        result = Controller().get_libraries_data(
            platform, owner, repo_name, release, wanted_data)

        # Assert that the returned dictionary only contains the Libraries.io data
        # and that the value is equal to the one we specified
        assert result == {"lib_release_frequency": 1, "lib_contributor_count": 5, "lib_dependency_count": 3,
                          "lib_dependent_count": 2, "lib_latest_release_date": "2016-04-20T04:09:15.000Z",
                          "lib_first_release_date": "2016-04-19T04:09:15.000Z", "lib_release_count": 2,
                          "lib_sourcerank": 5, "unknown": None}

    @mock.patch('src.cve.cve_spider.CVESpider.get_cve_vulnerability_count')
    @mock.patch('src.cve.cve_spider.CVESpider.get_all_cve_data')
    @mock.patch('src.cve.cve_spider.CVESpider.get_cve_codes')
    def test_get_cve_data(self, mock_codes: mock.Mock, mock_all_data: mock.Mock, mock_vulnerability_count: mock.Mock) -> None:
        """
        Test for the get_cve_data function.
        """
        # Set the required inputs
        repo_name = 'numpy'
        wanted_data = ['cve_count',
                       'cve_vulnerabilities', 'cve_codes', 'unknown']

        # Set the mock return values for the functions we are testing
        mock_vulnerability_count.return_value = 1
        mock_all_data.return_value = [1, 2, 3, 4]
        mock_codes.return_value = [1, 2, 3]

        # Run the function we are testing
        result = Controller().get_cve_data(repo_name, wanted_data)

        # Assert that the returned dictionary contains the CVE data
        # and that the value is equal to the one we specified
        assert result == {"cve_count": 1, "cve_vulnerabilities": [
            1, 2, 3, 4], "cve_codes": [1, 2, 3], "unknown": None}

    @mock.patch('src.stackoverflow.stackoverflow_spider.StackOverflowSpider.get_monthly_popularity')
    def test_get_so_data(self, mock_stackoverflow: mock.Mock) -> None:
        """
        Test for the get_so_data function.
        """
        # Set the required inputs
        repo_name = 'numpy'
        wanted_data = ['so_popularity', 'unknown']

        # Setup the mocking
        mock_stackoverflow.return_value = tuple([0, 1, 2])

        # run the controller with the input JSON
        result = Controller().get_so_data(repo_name, wanted_data)

        # Assert that the returned dictionary only contains the Stack Overflow data
        # and that the value is equal to the one we specified
        assert result == {'so_popularity': tuple([0, 1, 2]), 'unknown': None}

    @mock.patch('src.github.github_api_calls.GitHubAPICall.get_release_download_links')
    @mock.patch('src.clamav.clamav_scanner.ClamAVScanner.get_virus_ratio')
    def test_get_virus_data(self, mock_clamav: mock.Mock, mock_github: mock.Mock) -> None:
        """
        Test for the get_virus_data function.
        """

        # Set the required inputs
        owner = 'numpy'
        repo_name = 'numpy'
        release = 'v1.22.1'
        wanted_data = ['virus_ratio', 'unknown']

        # Setup the mocking
        mock_github.return_value = ['']
        mock_clamav.return_value = 0.0

        # Run the controller with the input JSON
        result = Controller().get_virus_data(owner, repo_name, release, wanted_data)

        # Assert that the returned dictionary only contains the virus ratio
        # and that the value of that ratio is equal to the one we specified
        assert result == {'virus_ratio': 0.0, 'unknown': None}


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
