"""
Allow the program to use the GitHub Device Flow in order to authenticate the user,
and get their OAuth token for API calls.
"""

# For request time-outs
import time
import dotenv
# For executing API calls
import requests


def authenticate_user(client_id):
    """
    Try to get a OAuth token for the user.
    If unsuccessful, it will return None.
    """

    # Request a device token from GitHub
    # This is used to request an OAuth token for the user.
    device_response = request_device_token_info(client_id)

    # See if we succesfully got a device token.
    # If not, tell the user, and exit.
    if device_response is None:
        print("Error: Could not get device token.")
        return False

    # If we did get a device token, try get the user's OAuth token.
    # Print the device verification code so the user can use it to get the OAuth token.
    print('User code: ' + device_response['user_code'])
    print('Verification URL: ' + device_response['verification_uri'])

    # Try to get the user's OAuth token.
    user_token = request_user_token(client_id, device_response)

    # See if we got an OAuth token.
    # If not, tell the user, and exit.
    if user_token is None:
        print("Error: Could not get user token.")
        return False

    # If we did get an OAuth token, return it.
    print("Successfully authenticated user.")

    # Write the token to the .env file
    dotenv.set_key(dotenv_path='.env', key_to_set='GITHUB_TOKEN',
                   value_to_set=user_token)

    return True


def request_device_token_info(client_id):
    """
    Request a device token from GitHub.
    """
    # Request the token using our client ID, with scope of public_repo to only target public repos.
    response = requests.post(
        'https://github.com/login/device/code',
        data={'client_id': client_id},
        headers={'Accept': 'application/json'}
    )

    # See if the post request was successful.
    # If not, tell the user, and exit.
    if response.status_code != 200:
        print("Error: " + response.text)
        return None
    # If we did get a response, return it
    return response.json()


def request_user_token(client_id, device_response):
    """Use the device token to get the user's OAuth token."""

    # Get some required information from the device response.
    # Interval is a github defined integer defining
    # the amount of seconds that need to be inbetween the requests.
    interval = device_response['interval']
    # Our device token
    device_token = device_response['device_code']
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

            return None

        # If we didn't get an error, return the token.
        return user_token_response['access_token']
