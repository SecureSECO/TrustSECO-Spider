"""
File containing the setup for the Flask application.

Running this file will start the Flask application on the localhost at port 5000.
"""

# Import Flask
from flask import Flask, make_response, request
# Import JSON for pretty printing
import json
# Import the controller of the TrustSECO-Spider
import controller


# Create the Flask application
app = Flask('app')


# Set the route for data-retrieval
@app.post('/get_data')
def get_data():
    """Uses the given JSON to get the wanted data-points."""

    # Get the input json
    input_json = request.get_json()
    # Inform the user of what is happening
    print('Received the following JSON:')
    print(json.dumps(input_json, indent=4))

    # Get the result from the spider
    result = controller.get_data(input_json)

    # Return the result
    response = make_response(result)
    if type(result) is str:
        response.headers.set('Content-Type', 'text/plain')
    else:
        response.headers.set('Content-Type', 'application/json')

    # Return the response
    return response


# Set the route for token setting
@app.post('/set_tokens')
def set_tokens():
    """Uses the given JSON to set the tokens."""

    # Get the input json
    input_json = request.get_json()

    # Inform the user of what is happening
    print('Setting tokens...')

    # Initialize an output string
    output = ''

    # If the github token is given, set it
    if 'github_token' in input_json:
        github_token = input_json['github_token']

        controller.update_token_gh(github_token)
        output += 'Github token set.\n'

    # If the librery token is given, set it
    if 'libraries_token' in input_json:
        libraries_token = input_json['libraries_token']

        controller.update_token_lib(libraries_token)
        output += 'Libraries token set.\n'

    # Inform the user of what happened
    if output == '':
        output = 'Token(s) not set! Please provide valid tokens.'

    print(output)
    return output


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)
