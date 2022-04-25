"""
File containing the unit tests for the libraries_io_api_calls.py file.
"""

# Import for testing
import responses
# Unit testing imports
import pytest
from unittest import mock
# Spider import
from LibrariesIO.libaries_io_api_calls import LibrariesAPICall
import constants


# region functions with actual API calls
class TestProjectInformation:
    """
    Class for testing the API call for getting the project information.

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
    """

    @responses.activate
    def test_valid_parameters(self):
        """
        Test for when the function receives the correct input parameters
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'Pypi'
        name = 'numpy'

        # Create the url, and add it to responses
        info_url = f'https://libraries.io/api/{platform}/{name}'
        responses.add(responses.GET, info_url, json={
                      'mock_data': 'value'}, status=200)

        # Execute the function
        response_data = lib_api_call.get_project_information(platform, name)

        # Check that the response is correct
        assert response_data == {'mock_data': 'value'}

    @responses.activate
    def test_invalid_parameters(self):
        """
        Test for when the function receives incorrect input parameters
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'Pypi'
        name = 'afesfse'

        # Create the url, and add it to responses
        info_url = f'https://libraries.io/api/{platform}/{name}'
        responses.add(responses.GET, info_url, json={
                      'error': 'not found'}, status=404)

        # Execute the function
        response_data = lib_api_call.get_project_information(platform, name)

        # Check that the response is correct
        assert response_data is None


class TestProjectDependencies:
    """
    Class for testing the API call for getting the project dependencies.

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
    """

    @responses.activate
    def test_valid_parameters(self):
        """
        Test for when the function receives the correct input parameters
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'Pypi'
        name = 'numpy'
        release = '1.22.3'

        # Create the url, and add it to responses
        info_url = f'https://libraries.io/api/{platform}/{name}/{release}/dependencies'
        print(info_url)
        responses.add(responses.GET, info_url, json={
                      'mock_data': 'value'}, status=200)

        # Execute the function
        response_data = lib_api_call.get_project_dependencies(
            platform, name, release)

        # Check that the response is correct
        assert response_data == {'mock_data': 'value'}

    @responses.activate
    def test_invalid_parameters(self):
        """
        Test for when the function receives incorrect input parameters
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'Pypi'
        name = 'faseigh'
        release = '1.22.3'

        # Create the url, and add it to responses
        depen_url = f'https://libraries.io/api/{platform}/{name}/{release}/dependencies'
        responses.add(responses.GET, depen_url, json={
                      'error': 'not found'}, status=404)

        # Execute the function
        response_data = lib_api_call.get_project_dependencies(
            platform, name, release)

        # Check that the response is correct
        assert response_data is None


class TestProjectRepository:
    """
    Class for testing the API call for getting the project repository.

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
    """

    @responses.activate
    def test_valid_parameters(self):
        """
        Test for when the function receives the correct input parameters
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        owner = 'numpy'
        name = 'numpy'

        # Create the url, and add it to responses
        info_url = f'https://libraries.io/api/github/{owner}/{name}'
        responses.add(responses.GET, info_url, json={
                      'mock_data': 'value'}, status=200)

        # Execute the function
        response_data = lib_api_call.get_project_repository(owner, name)

        # Check that the response is correct
        assert response_data == {'mock_data': 'value'}

    @responses.activate
    def test_invalid_parameters(self):
        """
        Test for when the function receives incorrect input parameters
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        owner = 'numpy'
        name = 'afesfse'

        # Create the url, and add it to responses
        info_url = f'https://libraries.io/api/github/{owner}/{name}'
        responses.add(responses.GET, info_url, json={
                      'error': 'not found'}, status=404)

        # Execute the function
        response_data = lib_api_call.get_project_repository(owner, name)

        # Check that the response is correct
        assert response_data is None
# endregion


# region look-up functions
class TestLookUp:
    """
    Class for testing the simple functions in the LibrariesAPICall class.
    These functions simply get a value from a dictionary using a specific key.

    The functions that are 'look-up' functions are:
    1. get_contributors_count
    2. get_dependent_count
    3. get_latest_release_date
    4. get_release_count
    5. get_sourcerank

    As these functions are very simple, we only test the following scenarios:
    1. get_project_repository returns None
    2. get_project_repository returns a dictionary, but without the wanted key
    3. get_project_repository returns a dictionary with the wanted key
    """

    @pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'github_contributions_count': 10}, 10)])
    def test_contributor_count(self, return_value, expected_value):
        """
        Test containing all of the possible scenarios
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        owner = 'numpy'
        name = 'numpy'

        with mock.patch('LibrariesIO.libaries_io_api_calls.LibrariesAPICall.get_project_repository', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_contributors_count(owner, name)

            # Check that the response is correct
            assert response_data == expected_value

    @pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'dependents_count': 10}, 10)])
    def test_dependents_count(self, return_value, expected_value):
        """
        Test containing all of the possible scenarios
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        owner = 'numpy'
        name = 'numpy'

        with mock.patch('LibrariesIO.libaries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_dependent_count(owner, name)

            # Check that the response is correct
            assert response_data == expected_value

    @pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'latest_release_published_at': 10}, 10)])
    def test_latest_release_date(self, return_value, expected_value):
        """
        Test containing all of the possible scenarios
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'numpy'
        name = 'numpy'

        with mock.patch('LibrariesIO.libaries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_latest_release_date(
                platform, name)

            # Check that the response is correct
            assert response_data == expected_value

    @pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'versions': [1, 2, 3]}, 3)])
    def test_release_count(self, return_value, expected_value):
        """
        Test containing all of the possible scenarios
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'numpy'
        name = 'numpy'

        with mock.patch('LibrariesIO.libaries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_release_count(platform, name)

            # Check that the response is correct
            assert response_data == expected_value

    @pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'rank': 10}, 10)])
    def test_sourcerank(self, return_value, expected_value):
        """
        Test containing all of the possible scenarios
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'numpy'
        name = 'numpy'

        with mock.patch('LibrariesIO.libaries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_sourcerank(platform, name)

            # Check that the response is correct
            assert response_data == expected_value
# endregion
