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

    def test_run_virus(self):
        """
        Test for when we only request virus data.
        """
