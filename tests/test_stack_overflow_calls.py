"""
File containing the unit tests for the Stack_Overflow_calls.py file.
"""

# Import for testing
import responses
# Unit testing imports
import pytest
# Import the Stackoverflow spider
from StackOverflow.stackoverflow_calls import StackOverflowCall


class TestTrends:
    """
    Class for testing trend responces

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
         "numpy": [2.1022945]}}, [(5, 2022, 2.1022945)]),
        ({"Month": [5], "TagPercents": {"numpy": [2.1022945]}}, None),
        ({"Year": [2022], "TagPercents": {"numpy": [2.1022945]}}, None),
        ({"Year": [2022], "Month": [5]}, None),
        ({"Year": [2022], "Month": [5], "TagPercents": None}, None)
    ])
    @pytest.mark.parametrize('package', ['numpy', 'nump'])
    def test_input(self, package, return_json, expected_value):
        """
        Test for when the function receives correct input parameters
        and test for when the function receives incorrect input parameters
        """

        # Create a Stack Overflow Call object
        stack_call = StackOverflowCall()

        # Add to responses
        responses.add(responses.GET, 'https://insights.stackoverflow.com/trends/get-data',
                      json=return_json, status=200)

        # Execute the function
        response_data = stack_call.get_monthly_trends(package)

        # Check that the response is correct based on the given package name
        if package == 'numpy':
            assert response_data == expected_value
        else:
            assert response_data is None

    @responses.activate
    def test_invalidreponse(self):
        """
        Test for when the function receives no response
        """

        # Create a Stack Overflow Call object
        stack_call = StackOverflowCall()
        # Add to responses
        responses.add(responses.GET, 'https://insights.stackoverflow.com/trends/get-data',
                      json={'error': 'not found'}, status=404)

        # Execute the function
        response_data = stack_call.get_monthly_trends('numpy')

        # Check that the response is correct based on the given package name
        assert response_data is None
