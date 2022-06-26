"""File containing the unit tests for the libraries_io_api_calls.py file."""

# Unit testing imports
import pytest
from unittest import mock
# Import for sending and handling HTTP requests
import responses
# Libraries.io API call import
from src.libraries_io.libraries_io_api_calls import LibrariesAPICall


class TestProjectInformation:
    """Class for testing the API call for getting the project information.

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
    """

    @responses.activate
    def test_valid_parameters(self) -> None:
        """Test for when the function receives the correct input parameters."""

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
    def test_invalid_parameters(self) -> None:
        """Test for when the function receives incorrect input parameters."""

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
    """Class for testing the API call for getting the project dependencies.

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
    """

    @responses.activate
    def test_valid_parameters(self) -> None:
        """Test for when the function receives the correct input parameters."""

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'Pypi'
        name = 'numpy'
        release = '1.22.3'

        # Create the url, and add it to responses
        info_url = f'https://libraries.io/api/{platform}/{name}/{release}/dependencies'

        responses.add(responses.GET, info_url, json={
                      'mock_data': 'value'}, status=200)

        # Execute the function
        response_data = lib_api_call.get_project_dependencies(
            platform, name, release)

        # Check that the response is correct
        assert response_data == {'mock_data': 'value'}

    @responses.activate
    def test_invalid_parameters(self) -> None:
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
    """Class for testing the API call for getting the project repository.

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
    """

    @responses.activate
    def test_valid_parameters(self) -> None:
        """Test for when the function receives the correct input parameters."""

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
    def test_invalid_parameters(self) -> None:
        """Test for when the function receives incorrect input parameters."""

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


class TestReleaseFrequency:
    """Class for testing the get_release_frequency function.

    This function depends on get_latest_release_date, get_first_release_date and get_release_count.

    To test this function, we will test the following scenarios:
    1. get_latest_release_date returns None
    2. get_first_release_date returns None
    3. get_release_count returns None
    4. All return a valid result
    """

    @pytest.mark.parametrize('latest_release_date, first_release_date, release_count, expected_result', [
        (None, None, None, None),
        ('2016-04-21T04:09:15.000Z', None, None, None),
        (None, '2016-04-20T04:09:15.000Z', None, None),
        (None, None, 1, None),
        ('2016-04-21T04:09:15.000Z', '2016-04-20T04:09:15.000Z', 1, 86400.0)
    ])
    def test_all(self, latest_release_date: str, first_release_date: str, release_count: int, expected_result: int) -> None:
        """
        Tests all of the possible scenarios

        Args:
            latest_release_date (str): The latest release date
            first_release_date (str): The first release date
            release_count (str): The number of releases
            expected_result (str): The expected result
        """

        # Set the input variables
        platform = 'Pypi'
        name = 'numpy'

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_latest_release_date', return_value=latest_release_date):
            with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_first_release_date', return_value=first_release_date):
                with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_release_count', return_value=release_count):
                    # Execute the function
                    result = lib_api_call.get_release_frequency(platform, name)

                    # Check that the response is correct
                    assert result == expected_result


class TestDependencyCount:
    """lass for testing the get_dependency_count function.

    This function depends on get_project_dependencies.

    To test this function, we will test the following scenarios:
    get_project_dependencies returns:
    1. None
    2. A dictionary without the wanted key
    3. A dictionary with the wanted key but no dependencies
    4. A dictionary with the wanted key and wrong dependencies
    5. A dictionary with the wanted key and dependencies
    """

    @pytest.mark.parametrize('return_value, expected_result', [
        (None, None),
        ({}, None),
        ({'dependencies': []}, 0),
        ({'dependencies': [{'efef': ''}]}, 0),
        ({'dependencies': [{'kind': 'Development'}, {'kind': ''}]}, 1)
    ])
    def test_all(self, return_value: dict, expected_result: int) -> None:
        """
        Tests all of the possible scenarios

        Args:
            return_value (dict): The return value of the get_project_dependencies function
            expected_result (int): The expected result
        """

        # Set the input variables
        platform = 'Pypi'
        name = 'numpy'
        release = '1.22.3'

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_dependencies', return_value=return_value):
            # Execute the function
            result = lib_api_call.get_dependency_count(platform, name, release)

            # Check that the response is correct
            assert result == expected_result


class TestFirstReleaseDate:
    """Class for testing the get_first_release_date function.

    To test this function, we will test the following scenarios:
    get_project_information returns:
    1. None
    2. A dictionary but without the wanted key
    3. A dictionary with the wanted key but no elements
    4. A dictionary with the wanted key and elements
    """

    @pytest.mark.parametrize('return_value, expected_result', [
        (None, None),
        ({}, None),
        ({'versions': []}, None),
        ({'versions': [
            {'published_at': '2016-04-20T04:09:15.000Z'}
        ]}, '2016-04-20T04:09:15.000Z'),
        ({'versions': [
            {'published_at': '2016-04-20T04:09:15.000Z'},
            {'published_at': '2016-04-21T04:09:15.000Z'}
        ]}, '2016-04-20T04:09:15.000Z')
    ])
    def test_all(self, return_value: dict, expected_result: str) -> None:
        """
        Tests all of the possible scenarios

        Args:
            return_value (dict): The return value of the get_project_information function
            expected_result (str): The expected result
        """

        # Set the input variables
        platform = 'Pypi'
        name = 'numpy'

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_information', return_value=return_value):
            # Execute the function
            result = lib_api_call.get_first_release_date(platform, name)

            # Check that the response is correct
            assert result == expected_result


class TestLookUp:
    """Class for testing the simple functions in the LibrariesAPICall class.

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

    @ pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'github_contributions_count': 10}, 10)])
    def test_contributor_count(self, return_value: dict, expected_value: int) -> None:
        """
        Test all of the possible scenarios for the get_contributors_count function

        Args:
            return_value (dict): The return value of the get_project_repository function
            expected_value (int): The expected value
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        owner = 'numpy'
        name = 'numpy'

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_repository', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_contributors_count(owner, name)

            # Check that the response is correct
            assert response_data == expected_value

    @ pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'dependents_count': 10}, 10)])
    def test_dependents_count(self, return_value: dict, expected_value: int) -> None:
        """
        Test all of the possible scenarios for the get_dependent_count function

        Args:
            return_value (dict): The return value of the get_project_repository function
            expected_value (int): The expected value
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        owner = 'numpy'
        name = 'numpy'

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_dependent_count(owner, name)

            # Check that the response is correct
            assert response_data == expected_value

    @ pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'latest_release_published_at': 10}, 10)])
    def test_latest_release_date(self, return_value: dict, expected_value: int) -> None:
        """
        Test all of the possible scenarios for the get_latest_release_date function

        Args:
            return_value (dict): The return value of the get_project_repository function
            expected_value (int): The expected value
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'numpy'
        name = 'numpy'

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_latest_release_date(
                platform, name)

            # Check that the response is correct
            assert response_data == expected_value

    @ pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'versions': [1, 2, 3]}, 3)])
    def test_release_count(self, return_value: dict, expected_value: int) -> None:
        """
        Test all of the possible scenarios for the get_release_count function

        Args:
            return_value (dict): The return value of the get_project_repository function
            expected_value (int): The expected value
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'numpy'
        name = 'numpy'

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_release_count(platform, name)

            # Check that the response is correct
            assert response_data == expected_value

    @ pytest.mark.parametrize('return_value, expected_value', [(None, None), ({}, None), ({'rank': 10}, 10)])
    def test_sourcerank(self, return_value: dict, expected_value: int) -> None:
        """
        Test all of the possible scenarios for the get_sourcerank function

        Args:
            return_value (dict): The return value of the get_project_repository function
            expected_value (int): The expected value
        """

        # Create a libraries.io API call object
        lib_api_call = LibrariesAPICall()

        # Set the input variables
        platform = 'numpy'
        name = 'numpy'

        with mock.patch('src.libraries_io.libraries_io_api_calls.LibrariesAPICall.get_project_information', new=mock.Mock(return_value=return_value)):
            # Execute the function
            response_data = lib_api_call.get_sourcerank(platform, name)

            # Check that the response is correct
            assert response_data == expected_value


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
