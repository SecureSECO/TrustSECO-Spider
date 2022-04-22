"""
File containing the unit tests for the api_calls.py file.
"""

# Import for testing
import responses
# Unit testing imports
import pytest
from unittest import mock
from requests.models import Response
# Spider imports
from api_calls.api_calls import make_api_call, get_needed_headers, get_needed_params
import constants


@mock.patch('api_calls.authentication.setup_environment', new=mock.Mock(return_value=None))
class TestMakeAPICall_gh:
    """
    Class for testing the actual API calls

    The following tests will be performed:
    1. Valid api key
    2. Invalid api key

    Both of these tests will get different permutations of input parameters like:
    - api_url and its return value
    - headers and no headers
    """

    @responses.activate
    @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', Response())])
    @mock.patch.dict('os.environ', {constants.GITHUB_TOKEN: 'test_key'})
    def test_valid_key(self, api_url, return_value):
        """
        Test the function making an API call with a valid API key
        """
        # Mock the API call for when the call is supposed to be successful
        if return_value is not None:
            responses.add(responses.GET, api_url, body='testing', status=200)

        # Make the API call
        actual_result = make_api_call(api_url, constants.API_GITHUB)

        # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
        assert isinstance(actual_result, type(return_value))

    @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', None)])
    @mock.patch.dict('os.environ', {constants.GITHUB_TOKEN: 'asdfs'})
    def test_invalid_key(self, api_url, return_value):
        """
        Test the function making an API call with an invalid API key
        """

        # Make the API call
        actual_result = make_api_call(api_url, constants.API_GITHUB)

        # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
        assert isinstance(actual_result, type(return_value))


@mock.patch('api_calls.authentication.setup_environment', new=mock.Mock(return_value=None))
class TestMakeAPICall_lib:
    """
    Class for testing the actual API calls

    The following tests will be performed:
    1. Valid api key
    2. Invalid api key

    Both of these tests will get different permutations of input parameters like:
    - api_url and its return value
    - headers and no headers
    """

    @responses.activate
    @pytest.mark.parametrize('api_url, return_value', [('https://libraries.io/api/platfs', None), ('https://libraries.io/api/platforms', Response())])
    @mock.patch.dict('os.environ', {constants.LIBRARIES_TOKEN: 'test_key'})
    def test_valid_key(self, api_url, return_value):
        """
        Test the function making an API call with a valid API key
        """
        # Mock the API call for when the call is supposed to be successful
        if return_value is not None:
            responses.add(responses.GET, api_url, body='testing', status=200)

        # Make the API call
        actual_result = make_api_call(api_url, constants.API_LIBRARIES)

        # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
        assert isinstance(actual_result, type(return_value))

    @pytest.mark.parametrize('api_url, return_value', [('https://libraries.io/api/platfs', None), ('https://libraries.io/api/platforms', None)])
    @mock.patch.dict('os.environ', {constants.LIBRARIES_TOKEN: '!$#@#$sdafjkh'})
    def test_invalid_key(self, api_url, return_value):
        """
        Test the function making an API call with an invalid API key
        """

        # Make the API call
        actual_result = make_api_call(api_url, constants.API_LIBRARIES)

        # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
        assert isinstance(actual_result, type(return_value))


@mock.patch.dict('os.environ', {constants.GITHUB_TOKEN: 'test_key'})
@pytest.mark.parametrize('api_type', [constants.API_GITHUB, constants.API_LIBRARIES])
class TestGetNeededHeaders:
    """
    Class for testing the function that gets the needed headers for the API calls

    As this function is very simple, we will only test the following:
    1. api_type is GitHub
    2. api_type is Libraries.io
    """

    def test_get_needed_headers(self, api_type):
        # Get the headers
        result = get_needed_headers(api_type)

        # Make sure the result matches what we expected
        if api_type == constants.API_GITHUB:
            assert isinstance(result, type({}))
        elif api_type == constants.API_LIBRARIES:
            assert result is None


@mock.patch.dict('os.environ', {constants.LIBRARIES_TOKEN: 'test_key'})
@pytest.mark.parametrize('api_type', [constants.API_GITHUB, constants.API_LIBRARIES])
class TestGetNeededParams:
    """
    Class for testing the function that gets the needed parameters for the API calls

    As this function is very simple, we will only test the following:
    1. api_type is GitHub
    2. api_type is Libraries.io
    """

    def test_get_needed_params(self, api_type):
        # Get the parameters
        result = get_needed_params(api_type)

        # Make sure the result matches what we expected
        if api_type == constants.API_GITHUB:
            assert result is None
        elif api_type == constants.API_LIBRARIES:
            assert isinstance(result, type({}))
