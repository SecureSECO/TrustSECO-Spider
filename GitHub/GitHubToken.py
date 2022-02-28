import requests
import time

# Try to get a OAuth token for the user.
# If unsuccessful, it will return None.
def authenticate_user(client_id, scope):
    # Request a device token from GitHub
    # This is used to request an OAuth token for the user.
    device_response = request_device_token_info(client_id, scope)

    # See if we succesfully got a device token.
    # If not, tell the user, and exit.
    if device_response == None:
        print("Error: Could not get device token.")
        return None
    # If we did get a device token, try get the user's OAuth token.
    else:
        # Print the device verification code so the user can use it to get the OAuth token.
        print('User code: ' + device_response['user_code'])

        # Try to get the user's OAuth token.
        user_token = request_user_token(client_id, device_response)

        # See if we got an OAuth token.
        # If not, tell the user, and exit.
        if user_token == None:
            print("Error: Could not get user token.")
            return None
        # If we did get an OAuth token, return it.
        else:
            return user_token

# Request a device token from GitHub.
def request_device_token_info(client_id, scope):
    # Request the token using our client ID, with scope of public_repo to only target public repos.
    response = requests.post('https://github.com/login/device/code', data={ 'scope' : scope, 'client_id' : client_id }, headers={ 'Accept' : 'application/json' })

    # See if the post request was successful.
    # If not, tell the user, and exit.
    if response.status_code != 200:
        print("Error: " + response.text)
        return None
    # If we did get a response, return it
    else:
        return response.json()

# Use the device token to get the user's OAuth token.
def request_user_token(client_id, device_response):
    # Get some required information from the device response.
    # Interval is a github defined integer defining the amount of seconds that need to be inbetween the requests.
    interval = device_response['interval']
    # Our device token
    device_token = device_response['device_code']
    # Grant type is a github defined string defining the type of token we are requesting.
    grant_type = 'urn:ietf:params:oauth:grant-type:device_code'

    # Loop until we either get the token, or get an error
    while True:
        # Get a response from GitHub.
        user_token_response_np = requests.post('https://github.com/login/oauth/access_token', data={ 'client_id' : client_id, 'device_code' : device_token, 'grant_type' : grant_type }, headers={ 'Accept' : 'application/json' })

        # Convert the response to a json object.
        user_token_response = user_token_response_np.json()

        # See if the response we got was an error.
        # If so, inform the user of whic error occured, and either sleep or exit.
        if 'error' in user_token_response:
            if user_token_response['error'] == 'authorization_pending':
                print("Waiting for verification...")
                time.sleep(interval)
                continue
            elif user_token_response['error'] == 'slow_down':
                print("Recieved slow-down error.")
                interval += 5;
                time.sleep(interval)
                continue
            elif user_token_response['error'] == 'expired_token':
                print("Error: Token expired.")
                return None
            elif user_token_response['error'] == 'unsupported_grant_type':
                print("Error: Unsupported grant type.")
                return None
            elif user_token_response['error'] == 'incorrect_client_credentials':
                print("Error: Incorrect client credentials.")
                return None
            elif user_token_response['error'] == 'incorrect_client_credentials':
                print("Error: Incorrect client credentials.")
                return None
            elif user_token_response['error'] == 'access_denied':
                print("Error: User denied access.")
                return None
            # Catch all for any other error.
            else:
                print("Error: " + user_token_response['error'])
                return None
        # If we didn't get an error, return the token.
        else:
            return user_token_response['access_token']