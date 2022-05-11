"""File containing all of the logic pertaining to making actual API calls

This file handles all of the logic for actually making API calls.
This allows the program to be more modular and easier to maintain.

    Typical usage:

    response = make_api_call(api_url, api_type)
"""

import os
import time
import requests
import constants
from dotenv import load_dotenv


def make_api_call(api_url, api_type) -> requests.Response:
    """
    Perform a simple GET request, based off the given URL

    Parameters:
        api_url (str): The URL to make the GET request to
        api_type (str): The type of API to make the request to

    Returns:
        response (obj): The response from the GET request
    """

    # Make sure the environment variables are loaded
    load_dotenv(dotenv_path=constants.ENVIRON_FILE, override=True)

    data_response = None

    # Catch any requests errors
    try:
        # Basic request to get the information.
        if api_type == constants.API_GITHUB:
            data_response = requests.get(
                api_url, headers=get_needed_headers(api_type))
        elif api_type == constants.API_LIBRARIES:
            data_response = requests.get(
                api_url, params=get_needed_params(api_type))
    except requests.exceptions.RequestException as error:
        print('Requests encountered an error:')
        print(error)
        return None

    # See if we got a valid response
    if data_response.status_code == 200:
        return data_response
    # See if we got a rate limit error
    elif data_response.status_code == 429:
        # See if the header includes the rate limit reset time
        # If so, use it
        if 'Retry-After' in data_response.headers:
            retry_time = data_response.headers['Retry-After']
            print(
                f'Too many requests. Trying again in {retry_time} seconds.')
            time.sleep(retry_time)
            return make_api_call(api_url)
        # If not, use 30 seconds, as it is half the rate limit reset time
        else:
            print('Too many requests. Trying again in 30 seconds.')
            time.sleep(30)
            return make_api_call(api_url)
    # Else, we got an unknown error so return None
    else:
        if api_type == constants.API_GITHUB:
            print('Unable to get data from GitHub.')
            print(f'Error: {data_response.status_code}')
            return None
        elif api_type == constants.API_LIBRARIES:
            print('Unable to get data from Libraries.io')
            print(f'Error: {data_response.status_code}')
            return None


def get_needed_headers(api_type) -> dict:
    """
    Gets the needed headers for the given API type

    Parameters:
        api_type (str): The type of API to make the request to

    Returns:
        headers (dict): The headers to use for the request
    """

    if api_type == constants.API_GITHUB:
        return {'Authorization': 'token ' + os.getenv(constants.GITHUB_TOKEN),
                'Accept': 'application/vnd.github.v3+json'}
    else:
        return None


def get_needed_params(api_type) -> dict:
    """
    Gets the needed parameters for the given API type

    Parameters:
        api_type (str): The type of API to make the request to

    Returns:
        params (dict): The parameters to use for the request
    """

    if api_type == constants.API_GITHUB:
        return None
    elif api_type == constants.API_LIBRARIES:
        return {'api_key': os.getenv(constants.LIBRARIES_TOKEN)}
    else:
        return None
