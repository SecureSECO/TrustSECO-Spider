"""
File containing the unit tests for the github_api_calls.py file.
"""


import json
# Unit testing imports
import responses
# Spider import
import GitHub.github_api_calls as api_caller

try:
    import github_constants as gc
except ImportError:
    import GitHub.github_constants as gc


class TestAPICall:
    """
    Testing for the general API call funtion.
    This function is used by all other functions in file, so it is important it works correctly.

    We will test the following scenario's:
    1. Invalid response code
    2. Invalid body
    3. Rate limit faults
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
    5. URL
        - Invalid URL
        - Valid URL
    6. Valid input
    """

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
