"""File containing the unit tests for the Stack_Overflow_calls.py file."""

# Unit testing imports
import pytest
# Import for sending and handling HTTP requests
import responses
# StackOverflow spider import
from src.stackoverflow.stackoverflow_spider import StackOverflowSpider


class TestTrends:
    """Class for testing Stack Overflow trend responces

    To test this function, we shall test the following scenarios:
    1. The input parameters are valid
    2. The input parameters are invalid
      - Year is missing
      - Month is missing
      - TagPercents is missing
      - Package is not in TagPercents
    3. The response is invalid
    """

    @responses.activate
    @pytest.mark.parametrize('return_json, expected_value', [
        ({"Year": [2022], "Month": [5], "TagPercents": {
         "numpy": [2.1022945]}}, (5, 2022, 0)),
        ({"Month": [5], "TagPercents": {"numpy": [2.1022945]}}, None),
        ({"Year": [2022], "TagPercents": {"numpy": [2.1022945]}}, None),
        ({"Year": [2022], "Month": [5]}, None),
        ({"Year": [2022], "Month": [5], "TagPercents": None}, None)
    ])
    def test_unknown_package(self, return_json: dict, expected_value: tuple) -> None:
        """
        Test for when the function receives an unknown package name

        Parameters:
            return_json (dict): The json to return from the API call
            expected_value (tuple): The expected value of the function
        """

        # Create a Stack Overflow Call object
        stack_call = StackOverflowSpider()

        # Add to responses
        responses.add(responses.GET, 'https://insights.stackoverflow.com/trends/get-data',
                      json=return_json, status=200)

        # Execute the function
        response_data = stack_call.get_monthly_popularity('nump')

        # Check that the response is correct based on the given package name
        assert response_data == expected_value

    @responses.activate
    @pytest.mark.parametrize('return_json, expected_value', [
        ({"Year": [2022], "Month": [5], "TagPercents": {
         "numpy": [2.1022945]}}, (5, 2022, 2.1022945)),
        ({"Month": [5], "TagPercents": {"numpy": [2.1022945]}}, None),
        ({"Year": [2022], "TagPercents": {"numpy": [2.1022945]}}, None),
        ({"Year": [2022], "Month": [5]}, None),
        ({"Year": [2022], "Month": [5], "TagPercents": None}, None)
    ])
    def test_valid_package(self, return_json: dict, expected_value: tuple) -> None:
        """
        Test for when the function receives a known package name.

        Parameters:
            return_json (dict): The json to return from the API call
            expected_value (tuple): The expected value of the function
        """

        # Create a Stack Overflow Call object
        stack_call = StackOverflowSpider()

        # Add to responses
        responses.add(responses.GET, 'https://insights.stackoverflow.com/trends/get-data',
                      json=return_json, status=200)

        # Execute the function
        response_data = stack_call.get_monthly_popularity('numpy')

        # Check that the response is correct based on the given package name
        assert response_data == expected_value

    @responses.activate
    def test_invalid_response(self) -> None:
        """
        Test for when the function receives no response
        """

        # Create a Stack Overflow Call object
        stack_call = StackOverflowSpider()
        # Add to responses
        responses.add(responses.GET, 'https://insights.stackoverflow.com/trends/get-data',
                      json={'error': 'not found'}, status=404)

        # Execute the function
        response_data = stack_call.get_monthly_popularity('numpy')

        # Check that the response is correct based on the given package name
        assert response_data is None


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
