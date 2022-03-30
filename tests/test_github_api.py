"""
File containing the unit tests for the github_api_calls.py file.
"""

import json
# Unit testing imports
import responses
import os
from unittest import mock
# Spider import
import GitHub.github_api_calls as api_caller
import GitHub.github_constants as gc


@mock.patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
class TestAPICall:
    """
    Testing for the general API call funtion.
    This function is used by all other functions in file, so it is important it works correctly.

    We will test the following scenario's:
    1. Invalid response code
    2. Rate limit faults
        - No more Core calls left
        - No more Search calls left
        - No more Rate calls left
    3. GitHub token
        - Found
        - Not Found
        - Valid
        - Invalid
    4. Header
        - No header
        - Invalid header
    5. Invalid URL
    6. Valid input
    """

    @responses.activate
    def test_invalid_response_code(self):
        """
        Testing for invalid response code.
        """

        test_url = 'https://api.github.com'

        responses.add(responses.GET, test_url, status=404)

        g = api_caller.GitHubAPICall(False)

        g.core_remaining = 100
        g.search_remaining = 100
        g.rate_remaining = 100

        result = g.make_api_call(test_url, gc.CORE)

        assert g.core_remaining == 99
        assert g.search_remaining == 100
        assert g.rate_remaining == 100
        assert result is None

    @mock.patch.object(api_caller.GitHubAPICall, 'set_rate_limit_data', new=mock.MagicMock())
    def test_rate_limit_core(self):
        """
        Testing the rate limit for the Core API.
        """

        url = 'http://test.com/'

        g = api_caller.GitHubAPICall(False)

        g.core_remaining = 0
        g.search_remaining = 100
        g.rate_remaining = 100

        result = g.make_api_call(url, gc.CORE)

        assert g.core_remaining == 0
        assert g.search_remaining == 100
        assert g.rate_remaining == 99
        mock.Mock.assert_called_once(g.set_rate_limit_data)
        assert result is None

    @mock.patch.object(api_caller.GitHubAPICall, 'set_rate_limit_data', new=mock.MagicMock())
    def test_rate_limit_search(self):
        """
        Testing the rate limit for the Core API.
        """

        url = 'http://test.com/'

        g = api_caller.GitHubAPICall(False)

        g.core_remaining = 100
        g.search_remaining = 0
        g.rate_remaining = 100

        result = g.make_api_call(url, gc.SEARCH)

        assert g.core_remaining == 100
        assert g.search_remaining == 0
        assert g.rate_remaining == 99
        mock.Mock.assert_called_once(g.set_rate_limit_data)
        assert result is None

    @mock.patch.object(api_caller.GitHubAPICall, 'set_rate_limit_data', new=mock.MagicMock())
    def test_rate_limit_rate(self):
        """
        Testing the rate limit for the Core API.
        """

        url = 'http://test.com/'

        g = api_caller.GitHubAPICall(False)

        g.core_remaining = 100
        g.search_remaining = 100
        g.rate_remaining = 0

        result = g.make_api_call(url, gc.RATE)

        assert g.core_remaining == 100
        assert g.search_remaining == 100
        assert g.rate_remaining == 0
        mock.Mock.assert_not_called(g.set_rate_limit_data)
        assert result is None

    @responses.activate
    def test_invalid_url(self):
        """
        Test a get request to an invalid URL
        """

        invalid_url = 'wibble://github.com'

        responses.add(responses.GET, invalid_url)

        g = api_caller.GitHubAPICall(False)

        # Make sure the rate variables are valid
        g.core_remaining = 100
        g.search_remaining = 100
        g.rate_remaining = 100

        # Make the "API call"
        result = g.make_api_call(invalid_url, gc.CORE)

        # Check the result
        assert g.core_remaining == 100
        assert g.search_remaining == 100
        assert g.rate_remaining == 100
        assert result is None

    @responses.activate
    def test_successfull_call(self):
        """
        Test the successfull call.
        """

        # Create the url
        api_url = 'https://api.github.com/repos/numpy/numpy'

        # Make sure we use our own fabricated response
        responses.add(responses.GET, api_url,
                      body='{"name": "numpy"}', status=200)

        g = api_caller.GitHubAPICall(False)

        # Make sure the rate variables are valid
        g.core_remaining = 100
        g.search_remaining = 100
        g.rate_remaining = 100

        # Make the "API call"
        result = g.make_api_call(api_url, gc.CORE)

        # Check the result
        assert result.status_code == 200
        assert g.core_remaining == 99
        assert g.search_remaining == 100
        assert g.rate_remaining == 100
        assert result.json() == json.loads('{"name": "numpy"}')
