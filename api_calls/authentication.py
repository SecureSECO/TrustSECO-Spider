import os
import time
import requests
from dotenv import load_dotenv, set_key
import constants


def setup_environment():
    # Make sure that the .env file exists, and has the proper key-values
    if not os.path.exists('.env'):
        print('Could not find .env file')
        print('Creating new .env file')
        with open('.env', 'w') as f:
            f.write(f'{constants.GITHUB_TOKEN}=\n{constants.LIBRARIES_TOKEN}=')

    # Authenticate the user
    authenticate_user()


def authenticate_user():
    """
    Authenticate the user for the GitHub and Libraries.io APIs
    """
    # (Re)load the environment variables before authenticating
    # To make sure that we can write tokens to the .env file
    load_dotenv(dotenv_path='.env', override=True)

    gh_authenticate_user()
    lib_authenticate_user()

    # (Re)load the environment variables after authenticating
    # To make sure the correct values are now present
    load_dotenv(dotenv_path='.env', override=True)


def gh_authenticate_user():
    """
    Authenticate the user for the GitHub API
    """

    # Return true if the token is already present
    if os.getenv(constants.GITHUB_TOKEN) is None or os.getenv(constants.GITHUB_TOKEN) == '':
        print('Starting GitHub authentication process')

        while True:
            # See if the authentication process succeeded
            # If so, continue with the API call
            if gh_get_token('1c3bf96ae6a2ec75435c'):
                print('Successfully authenticated user')
                # Reload the environment variables
                # As otherwise the GitHub token would not have been updated
                load_dotenv(dotenv_path='.env', override=True)

                break
            # If not, stop the program
            else:
                print('Authentication failed.')


def gh_get_token(client_id):
    """
    Try to get a OAuth token for the user.
    If unsuccessful, it will return None.
    """

    # Request a device token from GitHub
    # This is used to request an OAuth token for the user.
    try:
        # Request the token using our client ID, with scope of public_repo to only target public repos.
        device_response = requests.post(
            'https://github.com/login/device/code',
            data={'client_id': client_id},
            headers={'Accept': 'application/json'}
        )
    except requests.exceptions.RequestException as error:
        print('Requests encountered an error:')
        print(error)
        return False

    # Make sure the request was successful
    if device_response.status_code == 200:
        print('Successfully received device token')
        device_data = device_response.json()
    else:
        print('Failed to receive device token')
        return False

    # If we did get a device token, try get the user's OAuth token.
    # Print the device verification code so the user can use it to get the OAuth token.
    print('User code: ' + device_data['user_code'])
    print('Verification URL: ' + device_data['verification_uri'])

    # Try to get the user's OAuth token.
    return request_user_token(
        client_id, device_data['interval'], device_data['device_code'])


def request_user_token(client_id, interval, device_token):
    """Use the device token to get the user's OAuth token."""

    # Grant type is a github defined string defining the type of token we are requesting.
    grant_type = 'urn:ietf:params:oauth:grant-type:device_code'

    # Loop until we either get the token, or get an error
    while True:
        # Get a response from GitHub.
        user_token_response_np = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': client_id,
                'device_code': device_token,
                'grant_type': grant_type
            },
            headers={
                'Accept': 'application/json'
            }
        )

        # Convert the response to a json object.
        user_token_response = user_token_response_np.json()

        # See if the response we got was an error.
        # If so, inform the user of whic error occured, and either sleep or exit.
        if 'error' in user_token_response:
            if user_token_response['error'] == 'authorization_pending':
                time.sleep(interval)
                continue

            if user_token_response['error'] == 'slow_down':
                print("Recieved slow-down error.")
                interval += 5
                time.sleep(interval)
                continue

            if user_token_response['error'] == 'expired_token':
                print("Error: Token expired.")
            elif user_token_response['error'] == 'unsupported_grant_type':
                print("Error: Unsupported grant type.")
            elif user_token_response['error'] == 'incorrect_client_credentials':
                print("Error: Incorrect client credentials.")
            elif user_token_response['error'] == 'incorrect_client_credentials':
                print("Error: Incorrect client credentials.")
            elif user_token_response['error'] == 'access_denied':
                print("Error: User denied access.")
            else:
                print("Error: " + user_token_response['error'])

            return False

        # If we did get an OAuth token, return it.
        print("Successfully authenticated user.")

        # Write the token to the .env file
        set_key(dotenv_path='.env', key_to_set='GITHUB_TOKEN',
                value_to_set=user_token_response['access_token'])

        # Reload the environment variables
        # As otherwise the environmental tokens would not have been updated
        load_dotenv(dotenv_path='.env', override=True)

        return True


def lib_authenticate_user():
    """
    Authenticate the user for the Libraries.io API
    """

    # Return true if the token is already present
    if os.getenv(constants.LIBRARIES_TOKEN) is None or os.getenv(constants.LIBRARIES_TOKEN) == '':
        print('Starting Libraries.io authentication process')

        while True:
            print('Please enter your token:')

            token = input()

            # See if the user entered a valid token
            # by making sure text has been entered
            # and that the entered text is alphanumeric
            if len(token) > 0 and token.isalnum():
                print('Received API token')
                """We should probably test this token via some kind of quick api call"""

                # Write the token to the .env file
                set_key('.env', 'LIBRARIES_TOKEN', token)

                # Reload the environment variables
                # As otherwise the environmental tokens would not have been updated
                load_dotenv(dotenv_path='.env', override=True)

                break
            # If not, stop the program
            else:
                print('Authentication failed.')
