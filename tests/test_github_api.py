"""
File containing the unit tests for the github_api_calls.py file.
"""

import json
from operator import getitem
# Unit testing imports
import responses
import os
from unittest import mock
# Spider import
import GitHub.github_api_calls as api_caller
import GitHub.github_constants as gc


class TestUpdateRateLimit:
    """
    Class for testing the function updating the rate limit counts

    The following tests will be performed:
    1. Valid request response
    2. Invalid request response (by way of using an invalid response code)
    """

    @mock.patch('GitHub.github_api_calls.GitHubAPICall.make_api_call')
    def test_valid_response(self, mock_object):
        """
        Test the function updating the rate limit counts with a valid response
        """
        expected_core_remaining = 4500
        expected_search_remaining = 4500

        mock_object().json.return_value = {'resources': {'core': {
            'remaining': expected_core_remaining}, 'search': {'remaining': expected_search_remaining}}}
        # Create a GitHubAPICall object, and make sure it is initialized correctly
        g = api_caller.GitHubAPICall()
        assert g.core_remaining == 0
        assert g.search_remaining == 0

        # Call the update function
        assert g.update_rate_limit_data()
        # Assert the limits were updated correctly
        assert g.core_remaining == expected_core_remaining
        assert g.search_remaining == expected_search_remaining

    @ mock.patch.object(api_caller.GitHubAPICall, 'make_api_call', new=mock.Mock(return_value=None))
    def test_invalid_response(self):
        """
        Test the function updating the rate limit counts with an invalid status code
        """
        # Create a GitHubAPICall object, and make sure it is initialized correctly
        g = api_caller.GitHubAPICall()
        assert g.core_remaining == 0
        assert g.search_remaining == 0

        # Call the update function
        assert g.update_rate_limit_data() is False
        # Assert the limits were updated correctly
        assert g.core_remaining == 0
        assert g.search_remaining == 0


class TestCheckRateLimit:
    """
    Class for testing the function checking the rate limit counts

    The following tests will be performed:
    1. Core > 0 and Search > 0
    2. Core == 0 and Search > 0
    3. Core > 0 and Search == 0
    4. Core == 0 and Search == 0
    All of these will be tested with both call types
    We will also check if update_rate_limit_data() is called (only once)
    """
    # @mock.patch('GitHub.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=True))


class TestMakeAPICall:
    """
    Class for testing the actual API calls

    The following tests will be performed:
    """
