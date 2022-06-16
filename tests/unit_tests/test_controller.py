"""File containing the unit tests for the controller module."""

# Imports for testing
import pytest
from unittest import mock
# Import the Controller class
from controller import Controller


class TestController:
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

    @mock.patch('controller.Controller.get_virus_data')
    def test_run_virus(self, mock_virus_data):
        """
        Test for when we only request virus data.
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
            "virus_scanning": [
                "virus_ratio"
            ]
        }

        # Set the expected values
        virus_ratio_ev = {'virus_ratio': 3}

        # Set the mock return value for the get_virus_data method
        mock_virus_data.return_value = virus_ratio_ev

        # Run the controller with the input JSON
        result = Controller().run(input_json)

        # Assert that the returned dictionary only contains the virus ratio
        # and that the value of that ratio is equal to the one we specified
        assert result == virus_ratio_ev
