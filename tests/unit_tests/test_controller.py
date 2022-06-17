"""File containing the unit tests for the controller module."""

# Imports for testing
import pytest
from unittest import mock
# Import the Controller class
from controller import Controller


class TestControllerRun:
    """Class containing the unit tests for the controller module."""

    def test_run_no_proj_info(self):
        """
        Test for when the project information is missing from the input JSON.
        """

    def test_run_missing_info(self):
        """
        Test for when a required field within the project information is missing from the input JSON.
        """

    def test_run_gh(self):
        """
        Test for when we only request GitHub data.
        """

    def test_run_lib(self):
        """
        Test for when we only request Libraries.io data.
        """

    def test_run_cve(self):
        """
        Test for when we only request CVE data.
        """

    def test_run_so(self):
        """
        Test for when we only request Stack Overflow data.
        """

    def test_run_virus(self):
        """
        Test for when we only request virus scan data.
        """


class TestControllerData:
    def test_get_github_data(self):
        """
        Test for the get_github_data function.
        """

    def test_get_libraries_data(self):
        """
        Test for the get_libraries_data function.
        """

    def test_get_cve_data(self):
        """
        Test for the get_cve_data function.
        """

    def test_get_so_data(self):
        """
        Test for the get_so_data function.
        """

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
