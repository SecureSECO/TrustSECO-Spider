"""File containing the unit tests for the github_api_calls.py file."""

# Unit testing imports
import pytest
from unittest import mock
# Import for sending and handling HTTP requests
import responses
# GitHub API call import
import src.github.github_api_calls as api_caller
# Imports for utilities
import src.utils.constants as constants


@mock.patch.dict('os.environ', {'GITHUB_TOKEN': ''})
class TestUpdateRateLimit:
    """Class for testing the function updating the rate limit counts

    The following tests will be performed:
    1. Valid request response
    2. Invalid request response (by way of using an invalid response code)
    """

    @responses.activate
    def test_valid_response(self) -> None:
        """Test the function updating the rate limit counts with a valid response"""

        expected_core_remaining = 4500
        expected_search_remaining = 4500

        # A mock response
        return_body = {'resources': {'core': {
            'remaining': expected_core_remaining}, 'search': {'remaining': expected_search_remaining}}}
        # Add the get request to the watcher
        responses.add(responses.GET, constants.BASE_URL_RATE,
                      json=return_body, status=200)

        # Create a GitHubAPICall object, and make sure it is initialized correctly
        g = api_caller.GitHubAPICall()
        assert g.core_remaining == 0
        assert g.search_remaining == 0

        # Call the update function
        assert g.update_rate_limit_data()
        # Assert the limits were updated correctly
        assert g.core_remaining == expected_core_remaining
        assert g.search_remaining == expected_search_remaining

    @responses.activate
    def test_invalid_response(self) -> None:
        """Test the function updating the rate limit counts with an invalid status code"""

        # A mock response
        return_body = {'resources': {'core': {
            'remaining': 50}, 'search': {'remaining': 50}}}
        # Add the get request to the watcher
        responses.add(responses.GET, constants.BASE_URL_RATE,
                      json=return_body, status=404)

        # Create a GitHubAPICall object, and make sure it is initialized correctly
        g = api_caller.GitHubAPICall()
        assert g.core_remaining == 0
        assert g.search_remaining == 0

        # Call the update function
        assert g.update_rate_limit_data() is False
        # Assert the limits were updated correctly
        assert g.core_remaining == 0
        assert g.search_remaining == 0


@pytest.mark.parametrize('call_type', [constants.CORE, constants.SEARCH])
class TestCheckRateLimit:
    """Class for testing the function checking the rate limit counts

    Attributes:
        call_type (str): The type of call to check the rate limit for

    The following tests will be performed:
    1. Core > 0 and Search > 0
    2. Core == 0 and Search > 0
    3. Core > 0 and Search == 0
    4. Core == 0 and Search == 0
    All of these will be tested with both call types
    The amount of times update_rate_limit_data() is called will also be checked.
    """

    def test_both_greater_zero(self, call_type) -> None:
        """
        Test the function checking the rate limit counts with both counts greater than zero

        Parameters:
            call_type (str): The type of call to check the rate limit for
        """

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('src.github.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=True)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 5000
            g.search_remaining = 5000

            # Assert the function returns True
            assert g.check_rate_limit(call_type) is True
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == 0

    @pytest.mark.parametrize('return_value', [True, False])
    def test_core_zero_search_greater(self, call_type, return_value) -> None:
        """
        Test the function checking the rate limit counts with core count == 0 and search count > 0

        Parameters:
            call_type (str): The type of call to check the rate limit for
            return_value (bool): The value to return from the mock patch
        """

        # Set the expected assert values
        # The function should return False if the call type is Core, and True if the call type is Search
        expected_return_value = (call_type != constants.CORE)
        # The function should call update_rate_limit_data() once if the call type is Core, and never if the call type is Search
        if call_type == constants.CORE:
            expected_update_call_count = 1
        elif call_type == constants.SEARCH:
            expected_update_call_count = 0

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('src.github.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=return_value)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 0
            g.search_remaining = 5000

            # Assert the function returns True
            assert g.check_rate_limit(call_type) == expected_return_value
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == expected_update_call_count

    @pytest.mark.parametrize('return_value', [True, False])
    def test_core_greater_search_zero(self, call_type, return_value) -> None:
        """
        Test the function checking the rate limit counts with core count > 0 and search count == 0

        Parameters:
            call_type (str): The type of call to check the rate limit for
            return_value (bool): The value to return from the mock patch
        """

        # Set the expected assert values
        # The function should return False if the call type is Search, and True if the call type is Core
        expected_return_value = (call_type != constants.SEARCH)
        # The function should call update_rate_limit_data() once if the call type is Search, and never if the call type is Core
        if call_type == constants.CORE:
            expected_update_call_count = 0
        elif call_type == constants.SEARCH:
            expected_update_call_count = 1

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('src.github.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=return_value)) as mock_patch:
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

        Parameters:
            call_type (str): The type of call to check the rate limit for
            return_value (bool): The value to return from the mock patch
        """

        # Set the expected assert values
        # The function should return False in both cases
        expected_return_value = False
        # The function should call update_rate_limit_data() once in both cases
        expected_update_call_count = 1

        # Patch the update_rate_limit_data function to return True
        # By doing this we can see if it is called during the test
        with mock.patch('src.github.github_api_calls.GitHubAPICall.update_rate_limit_data', new=mock.Mock(return_value=return_value)) as mock_patch:
            # Create a GitHubAPICall object, and make sure it is initialized correctly
            g = api_caller.GitHubAPICall()
            g.core_remaining = 0
            g.search_remaining = 0

            # Assert the function returns True
            assert g.check_rate_limit(call_type) == expected_return_value
            # Assert the update_rate_limit_data function was not called
            assert mock_patch.call_count == expected_update_call_count


@mock.patch('src.utils.api_calls.make_api_call', new=mock.Mock(return_value=True))
@pytest.mark.parametrize('call_type', [constants.CORE, constants.SEARCH])
class TestTryAPICall:
    """Class for testing the API calling interface function

    As this function is quite simple, we will only have to test a few things:
    1. Try to perform an API call with a high enough rate limit
    2. Try to perform an API call with a too low rate limit

    The main thing to check here is that the rate limit counters are decremented correctly (if needed)
    """

    @mock.patch.dict('os.environ', {'GITHUB_TOKEN': ''})
    @mock.patch('src.github.github_api_calls.GitHubAPICall.check_rate_limit', new=mock.Mock(return_value=True))
    def test_valid_rate_limit(self, call_type) -> None:
        """
        Test the function making an API call with a valid rate limit

        Parameters:
            call_type (str): The type of call to make
        """

        # Set up the GitHubAPICall object
        g = api_caller.GitHubAPICall()
        g.core_remaining = 5000
        g.search_remaining = 5000

        # Execute the function
        actual_result = g.try_perform_api_call(
            constants.BASE_URL_RATE, call_type)

        # Assert that the function returns the correct value
        assert actual_result is None
        # Assert that the correct rate limit variable was decremented
        if call_type == constants.CORE:
            assert g.core_remaining == 4999
            assert g.search_remaining == 5000
        elif call_type == constants.SEARCH:
            assert g.core_remaining == 5000
            assert g.search_remaining == 4999

    @mock.patch('src.github.github_api_calls.GitHubAPICall.check_rate_limit', new=mock.Mock(return_value=False))
    def test_invalid_rate_limit(self, call_type) -> None:
        """
        Test the function making an API call with an invalid rate limit

        Parameters:
            call_type (str): The type of call to make
        """

        # Set up the GitHubAPICall object
        g = api_caller.GitHubAPICall()
        g.core_remaining = 5000
        g.search_remaining = 5000

        # Execute the function
        actual_result = g.try_perform_api_call('', call_type)

        # Assert that the function returns the correct value
        assert actual_result is None
        # Assert that no rate limit was decremented
        assert g.core_remaining == 5000
        assert g.search_remaining == 5000


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
