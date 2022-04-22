# import os
# # Import for testing
# import responses
# # Unit testing imports
# import pytest
# from unittest import mock
# from requests.models import Response
# # Spider import
# from api_calls.api_calls import make_api_call


# @pytest.mark.parametrize('given_headers', [None, {'test': 'test'}])
# class TestMakeAPICall:
#     """
#     Class for testing the actual API calls

#     The following tests will be performed:
#     1. Valid api key
#     2. Invalid api key

#     Both of these tests will get different permutations of input parameters like:
#     - api_url and its return value
#     - headers and no headers
#     """

#     @responses.activate
#     @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', Response())])
#     @mock.patch.dict('os.environ', {'GITHUB_TOKEN': 'test_key'})
#     def test_valid_key(self, api_url, return_value, given_headers):
#         """
#         Test the function making an API call with a valid API key
#         """
#         # Mock the API call for when the call is supposed to be successful
#         if return_value is not None:
#             responses.add(responses.GET, api_url, body='testing', status=200)

#         # Make the API call
#         actual_result = make_api_call(api_url, given_headers)

#         # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
#         assert isinstance(actual_result, type(return_value))

#     @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', None)])
#     @mock.patch.dict('os.environ', {'GITHUB_TOKEN': 'asdfs'})
#     def test_invalid_key(self, api_url, return_value, given_headers):
#         """
#         Test the function making an API call with an invalid API key
#         """

#         # Make the API call
#         actual_result = make_api_call(api_url, given_headers)

#         # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
#         assert isinstance(actual_result, type(return_value))

#     @pytest.mark.parametrize('api_url, return_value', [('https://api.github.com/repos/numpy/numpasfdy', None), ('https://api.github.com/repos/numpy/numpy', None)])
#     @mock.patch('GitHub.github_get_token.GitHubToken.authenticate_user', new=mock.Mock(return_value=False))
#     def test_no_key(self, api_url, return_value, given_headers):
#         """
#         Test the function making an API call, but there is no API key
#         """
#         # Remove the .env file if it exists
#         if os.path.exists('.env'):
#             os.remove('.env')

#         # Make the API call
#         actual_result = make_api_call(api_url, given_headers)

#         # Assert that the type of the result is the same as the wanted type (as we can't predict the exact return value)
#         assert isinstance(actual_result, type(None))
