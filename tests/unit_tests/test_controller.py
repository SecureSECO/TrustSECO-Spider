"""File containing the unit tests for the controller module."""

# Imports for testing
import pytest
from unittest import mock
# Import the Controller class
from controller import Controller


class TestControllerRun:
    """Class containing the unit tests for the controller module."""

    # create global variables for the input JSONs
    platform = 'Pypi'
    owner = 'numpy'
    repo_name = 'numpy'
    release = 'v1.22.1'

    def test_run_no_proj_info(self):
        """
        Test for when the project information is missing from the input JSON.
        """
        # make an input JSON with no project information
        input_json = {}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Check that the response is correct
        assert result == {'Error': 'Error: no project information found'}

    @pytest.mark.parametrize('input_json', [
        {"project_info": {
            "project_owner": owner,
            "project_name": repo_name,
            "project_release": release}},
        {"project_info": {
            "project_platform": platform,
            "project_name": repo_name,
            "project_release": release}},
        {"project_info": {
            "project_platform": platform,
            "project_owner": owner,
            "project_release": release}},
        {"project_info": {
            "project_platform": platform,
            "project_owner": owner,
            "project_name": repo_name}}
    ])
    def test_run_missing_info(self, input_json: dict) -> None:
        """
        Test for when a required field within the project information is missing from the input JSON.

        Parameters:
            input_json (dict): The input json to run the controller with
        """

        # Run the controller with the input JSON
        response_data = Controller().run(input_json)

        # Assert that the returned error is equal to the defined error in the controller
        assert response_data == {'Error': 'missing project information'}

    @mock.patch('controller.Controller.get_github_data', new=mock.Mock(return_value={"gh": "mock"}))
    def test_run_gh(self):
        """
        Test for when we only request GitHub data.
        """

        # make an input JSON with only requesting GitHub data
        input_json = {"project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
            "project_year": 2021},
            "gh_data_points": ["gh_contributor_count"]}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the Github data
        # and that the value is equal to the one we specified
        assert result == {"gh": "mock"}

    @mock.patch('controller.Controller.get_libraries_data', new=mock.Mock(return_value={"lb": "mock"}))
    def test_run_lib(self):
        """
        Test for when we only request Libraries.io data.
        """

        # make an input JSON with only requesting Libraries.io data
        input_json = {"project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
            "project_year": 2021},
            "lib_data_points": ["lib_release_frequency"]}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the Libraries.io data
        # and that the value is equal to the one we specified
        assert result == {"lb": "mock"}

    @mock.patch('controller.Controller.get_cve_data', new=mock.Mock(return_value={"cve": "mock"}))
    def test_run_cve(self):
        """
        Test for when we only request CVE data.
        """

        # make an input JSON with only requesting CVE data
        input_json = {"project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
            "project_year": 2021},
            "cve_data_points": ["cve_count"]}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the CVE data
        # and that the value is equal to the one we specified
        assert result == {"cve": "mock"}

    @mock.patch('controller.Controller.get_so_data', new=mock.Mock(return_value={"so": "mock"}))
    def test_run_so(self):
        """
        Test for when we only request Stack Overflow data.
        """

        # make an input JSON with only requesting Stack Overflow data
        input_json = {"project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
            "project_year": 2021},
            "so_data_points": ["so_popularity"]}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the Stack Overflow data
        # and that the value is equal to the one we specified
        assert result == {"so": "mock"}

    @mock.patch('controller.Controller.get_virus_data', new=mock.Mock(return_value={"virus": "mock"}))
    def test_run_virus(self):
        """
        Test for when we only request virus scan data.
        """

        # make an input JSON with only requesting virus scan data
        input_json = {"project_info": {
            "project_platform": "Pypi",
            "project_owner": "numpy",
            "project_name": "numpy",
            "project_release": "v1.22.1",
            "project_year": 2021},
            "virus_scanning": ["virus_ratio"]}

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the virus scan data
        # and that the value is equal to the one we specified
        assert result == {"virus": "mock"}


class TestControllerData:
    def test_get_github_data(self):
        """
        Test for the get_github_data function.
        """

    def test_get_libraries_data(self):
        """
        Test for the get_libraries_data function.
        """

    @mock.patch('src.cve.cve_spider.CVESpider.get_cve_vulnerability_count')
    @mock.patch('src.cve.cve_spider.CVESpider.get_all_cve_data')
    @mock.patch('src.cve.cve_spider.CVESpider.get_cve_codes')
    def test_get_cve_data(self, mock_codes, mock_all_data, mock_vulnerability_count):
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
    def test_get_so_data(self, mock_stackoverflow):
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
    def test_get_virus_data(self, mock_clamav, mock_github):
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
