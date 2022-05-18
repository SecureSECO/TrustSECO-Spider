"""File containing the setup for the Flask application.

Running this file will start the Flask application on the localhost at port 5000.
"""

# Import Flask
from flask import Flask, make_response, request
# Import JSON for pretty printing
import json
# Import the controller of the TrustSECO-Spider
import controller
# Import CORS needed
from flask_cors import CORS


# Create the Flask application
app = Flask('app')
# Enable CORS
CORS(app)


def purely_for_testing():
    return None

# Set the route for data-retrieval


@app.post('/get_data')
def get_data():
    """Uses the given JSON to get the wanted data-points."""

    # Try to get the input json
    (is_valid, data) = try_get_json_input()
    if not is_valid:
        return data
    else:
        input_json = data

    # Inform the user of what is happening
    print('Received the following JSON:')
    print(json.dumps(input_json, indent=4))

    # Get the result from the spider
    result = controller.get_data(input_json)

    # Return the result
    if 'Error' in result:
        response = make_response(result['Error'], 400)
        response.headers.set('Content-Type', 'text/plain')
    else:
        response = make_response(json.dumps(result), 200)
        response.headers.set('Content-Type', 'application/json')

    # Return the response
    return response


# Set the route for token setting
@app.post('/set_tokens')
def set_tokens():
    """Uses the given JSON to set the tokens."""

    # Try to get the input json
    (is_valid, data) = try_get_json_input()
    if not is_valid:
        return data
    else:
        input_json = data

    # Inform the user of what is happening
    print('Setting tokens...')

    # Initialize an output string
    output = ''

    # If the github token is given, set it
    if 'github_token' in input_json:
        github_token = input_json['github_token']

        controller.update_token_gh(github_token)
        output += 'Github token set. '

    # If the library token is given, set it
    if 'libraries_token' in input_json:
        libraries_token = input_json['libraries_token']

        controller.update_token_lib(libraries_token)
        output += 'Libraries token set.'

    # Inform the user of what happened
    if output == '':
        output = 'Token(s) not set! Please provide valid tokens.'
    print(output)

    # Return the output
    response = make_response(output)
    response.headers.set('Content-Type', 'text/plain')
    return response


def try_get_json_input():
    """Tries to get the JSON input from the request."""

    # Make sure the request is JSON
    if not request.is_json:
        output = 'Not a JSON request'
        print(output)
        response = make_response(output, 400)
        response.headers.set('Content-Type', 'text/plain')
        return (False, response)

    # Get the input json
    input_json = request.get_json()

    # Make sure the input is valid
    if input_json is None:
        output = 'Received invalid JSON'
        print(output)
        response = make_response(output, 400)
        response.headers.set('Content-Type', 'text/plain')
        return (False, response)

    # Return the input json only if it is valid
    return (True, input_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
