"""
File containing the unit tests for the github_api_calls.py file.
"""

# Import for
from requests.models import Response
# Unit testing imports
import pytest
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
    def test_valid_response(self, mock_make_api_call):
        """
        Test the function updating the rate limit counts with a valid response
        """
        expected_core_remaining = 4500
        expected_search_remaining = 4500

        mock_make_api_call().json.return_value = {'resources': {'core': {
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


@pytest.mark.parametrize('call_type', [gc.CORE, gc.SEARCH])
class TestCheckRateLimit:
    """
    Class for testing the function checking the rate limit counts

    The following tests will be performed:
    1. Core > 0 and Search > 0
    2. Core == 0 and Search > 0
    3. Core > 0 and Search == 0
    4. Core == 0 and Search == 0
    All of these will be tested with both call types
    We will also check if update_rate_limit_data() is called the correct amount of times
    """

    def test_both_greater_zero(self, call_type):
        """
        Test the function checking the rate limit counts with both counts greater than zero
        The function should always return true in this case, as it only does a simple boolean check
        """

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('GitHub.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=True)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 5000
            g.search_remaining = 5000

            # Assert the function returns True
            assert g.check_rate_limit(call_type) is True
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == 0

    @pytest.mark.parametrize('return_value', [True, False])
    def test_core_zero_search_greater(self, call_type, return_value):
        """
        Test the function checking the rate limit counts with core count == 0 and search count > 0
        The function should return True for call_type Search, as in that case there is only a simple boolean check
        If the call_type is Core, the function should return False as the actual count does not get updated
        """

        # Set the expected assert values
        # The function should return False if the call type is Core, and True if the call type is Search
        expected_return_value = (call_type != gc.CORE)
        # The function should call update_rate_limit_data() once if the call type is Core, and never if the call type is Search
        if call_type == gc.CORE:
            expected_update_call_count = 1
        elif call_type == gc.SEARCH:
            expected_update_call_count = 0

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('GitHub.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=return_value)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 0
            g.search_remaining = 5000

            # Assert the function returns True
            assert g.check_rate_limit(call_type) == expected_return_value
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == expected_update_call_count

    @pytest.mark.parametrize('return_value', [True, False])
    def test_core_greater_search_zero(self, call_type, return_value):
        """
        Test the function checking the rate limit counts with core count > 0 and search count == 0
        The function should return True for call_type Core, as in that case there is only a simple boolean check
        If the call_type is Search, the function should return False as the actual count does not get updated
        """

        # Set the expected assert values
        # The function should return False if the call type is Search, and True if the call type is Core
        expected_return_value = (call_type != gc.SEARCH)
        # The function should call update_rate_limit_data() once if the call type is Search, and never if the call type is Core
        if call_type == gc.CORE:
            expected_update_call_count = 0
        elif call_type == gc.SEARCH:
            expected_update_call_count = 1

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('GitHub.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=return_value)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 5000
            g.search_remaining = 0

            # Assert the function returns True
            assert g.check_rate_limit(call_type) == expected_return_value
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == expected_update_call_count

    @pytest.mark.parametrize('return_value', [True, False])
    def test_core_zero_search_zero(self, call_type, return_value):
        """
        Test the function checking the rate limit counts with core count == 0 and search count == 0
        The function should return False in both cases, as neither will be updated, and thus remain at count 0
        """

        # Set the expected assert values
        # The function should return False in both cases
        expected_return_value = False
        # The function should call update_rate_limit_data() once in both cases
        expected_update_call_count = 1

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('GitHub.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=return_value)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 0
            g.search_remaining = 0

            # Assert the function returns True
            assert g.check_rate_limit(call_type) == expected_return_value
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == expected_update_call_count


@pytest.mark.parametrize('given_headers', [None, {'test': 'test'}])
class TestMakeAPICall:
    """
    Class for testing the actual API calls

    The following tests will be performed:
    1. Valid api key
    2. Invalid api key

    Both of these tests will get different permutations of input parameters like:
    - api_url and its return value
    - headers and no headers
    """
    # @mock.patch.dict('os.environ', {'GITHUB_API_KEY': 'test_key'})
    # @mock.patch('GitHub.github_get_token.authenticate_user', new=mock.Mock(return_value=True))

    @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', Response())])
    def test_valid_key(self, api_url, return_value, given_headers):
        """
        Test the function making an API call with a valid API key
        """
        # Create a GitHubAPICall object
        g = api_caller.GitHubAPICall()

        # Make the API call
        actual_result = g.make_api_call(api_url, given_headers)

        # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
        assert isinstance(actual_result, type(return_value))

    @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', None)])
    @mock.patch.dict('os.environ', {'GITHUB_TOKEN': 'asdfs'})
    def test_invalid_key(self, api_url, return_value, given_headers):
        """
        Test the function making an API call with an invalid API key
        """
        # Create a GitHubAPICall object
        g = api_caller.GitHubAPICall()

        # Make the API call
        actual_result = g.make_api_call(api_url, given_headers)

        # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
        assert isinstance(actual_result, type(return_value))


@mock.patch('GitHub.github_api_calls.GitHubAPICall.make_api_call', new=mock.Mock(return_value=True))
@pytest.mark.parametrize('call_type', [gc.CORE, gc.SEARCH])
class TestTryAPICall:
    """
    Class for testing the API calling interface function

    As this function is quite simple, we will only have to test a few things:
    1. Try to perform an API call with a high enough rate limit
    2. Try to perform an API call with a too low rate limit

    The main thing to check here is that the rate limit counters are decremented correctly (if needed)
    """

    @mock.patch('GitHub.github_api_calls.GitHubAPICall.check_rate_limit', new=mock.Mock(return_value=True))
    def test_valid_rate_limit(self, call_type):
        """
        Test the function making an API call with a valid rate limit
        """

        # Set up the GitHubAPICall object
        g = api_caller.GitHubAPICall()
        g.core_remaining = 5000
        g.search_remaining = 5000

        # Execute the function
        actual_result = g.try_api_call('', call_type)

        # Assert that the function returns the correct value
        assert actual_result is True
        # Assert that the correct rate limit variable was decremented
        if call_type == gc.CORE:
            assert g.core_remaining == 4999
            assert g.search_remaining == 5000
        elif call_type == gc.SEARCH:
            assert g.core_remaining == 5000
            assert g.search_remaining == 4999

    @mock.patch('GitHub.github_api_calls.GitHubAPICall.check_rate_limit', new=mock.Mock(return_value=False))
    def test_invalid_rate_limit(self, call_type):
        """
        Test the function making an API call with an invalid rate limit
        """

        # Set up the GitHubAPICall object
        g = api_caller.GitHubAPICall()
        g.core_remaining = 5000
        g.search_remaining = 5000

        # Execute the function
        actual_result = g.try_api_call('', call_type)

        # Assert that the function returns the correct value
        assert actual_result is None
        # Assert that no rate limit was decremented
        assert g.core_remaining == 5000
        assert g.search_remaining == 5000
