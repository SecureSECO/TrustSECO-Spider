# TrustSECO-Spider
 
This spider uses a combination of actual spidering (using BeautifulSoup) and API calls (using requests) in order to gather information from GitHub and Libraries.io.
 
## GitHub
 
Our program retrieves most data-points using GitHub's REST API. Sadly, not all of the wanted data-points were accessible this way. In order to still gather this data, spidering had to be used.
 
It can currently get the following data-points from GitHub:
 
- Repository information:
  - Number of contributors
  - Number of users
  - Number of downloads
    - Per release
    - In total
  - Number of commits per year:
    - In the past year from the current date
    - In a specific year
  - Repository language
  - GitStar ranking
- Issues information:
  - Number of open issues
  - Number of issues without a response
  - Number of issues of a specific release
  - Ratio of open to closed issues
  - Average issue resolution time
- Owner information:
  - Number of stargazers
 
## Libraries.io

All of the data-points are gathered using various Libraries.io's APIs.

The currently available data-points are:

- Project:
  - Release frequency
  - Number of dependencies
  - Number of dependents
  - Number of releases
  - Latest release date
  - First release date
  - Sourcerank
- Repository:
  - Contributor count

## CVE

The spider can currently query the CVE service, and get all the known CVE codes of vulnerabilities of the given package.

For each of these codes, it can get the following information:

- CVE ID
- Vulnerability score
- Affected versions:
  - Start version
  - End version
  - The type thereof (inclusive or exclusive)

## How to use
 
### Requirements

In order to run our program, certain python libraries will have to be installed. This can easily be done by running the `pip install -r requirements.txt` command from within the `TrustSECO-Spider` folder.

### Running as a service

As the other sub-projects will need to request data from the spider, flask was used in order to create an endpoint for this. In order to run the TrustSECO-Spider as a (development) service, simply run `python .\app.py` command from within the `TrustSECO-Spider` folder.
This will run a local server on the following address: `http://localhost:5000`.

### Setting API tokens

After running the program as a service as described above, the API tokens for GitHub and Libraries.io must be set. This can be done by sending a POST request to `http://localhost:5000/set_tokens`. This POST request **must** contain the following:
1. A header with the content-type set as `application/json`.
2. A JSON input following the schemas found in the `JSON schemas` folder. The relevant JSON file would be `token_input.json`.

An example of this (using `python` and the `requests` library) would be the following:
```
header = {'Content-type':'application/json'}

input_json = {
  'github_token': 'gho_jeshfuehfhsjfe',
  'libraries_token': 'jdf9328bf87831bfdjs0823'
}

response = requests.post('http://localhost:5000/set_tokens', headers={'Content-type':'application/json'}, json=json_input)

print(response.text)
```
*Naturally, the tokens provided here are fake, and must be replaced with your own.*

If only 1 token has to be set/updated, only that 1 token needs to be supplied.

### Requesting data

This address can then be used in order to request data. This is done by sending a POST request to the endpoint. This POST request **must** contain the following:
1. A header with the content-type set as `application/json`.
2. A JSON input following the schemas found in the `JSON schemas` folder. The relevant JSON files would be `input_example.json` and `input_structure.json`.

An example of this (using `python` and the `requests` library) would be the following:
```
header = {'Content-type':'application/json'}

input_json = {
  'project_info': {
    'project_platform': 'Pypi', 
    'project_owner': 'numpy', 
    'project_name': 'numpy', 
    'project_release': 'v.1.22.1', 
    'project_year': 2021
  }, 
  'cve_data_points': [
    'cve_count',
    'cve_vulnerabilities',
    'cve_codes'
  ]
}

response = requests.post('http://localhost:5000/get_data', headers={'Content-type':'application/json'}, json=json_input)

print(response.json())
```

### Return values

Depending on which end-point you send a request to (`get_data` or `set_tokens`), a certain type of response will be sent.

In case of `set_tokens`, it will always return `Content-type: text/plain`.

In case of `get_data`, the return type will change depending on whether or not the request succeeded. For example, if the request did not contain all the needed information, the return type would be `Content-type: text/plain` and would contain the reason for the failure (in this case `Error: missing project information`).

If the request did succeed, the return type would be `Content-type: application/json`, and the response would include the wanted data in a JSON format.

Please use the content type to avoid trying to grab non-existent JSON data or text.

### Demo
 
This project also contains a small demo file (demo.py) which can demo basic functionality. Simply enter `python .\demo.py` in the command line in order to get a list of possible arguments. With these arguments you can specify which of the demos to run.
 
Depending on the given arguments, the demo will grab all of the available GitHub and Libraries.io data-points, and print them to the console.
Current commands:
 
- `python .\demo.py numpy` -> Gets all the data-points for the numpy package/repository
- `python .\demo.py afnetworking` -> Gets all the data-points for the AFNetworking package/repository
- `python .\demo.py all` -> Gets all the data-points for both numpy and AFNetworking
 
### Unit tests
 
The project also contains some of the unit tests too. These can be started from within the main `TrustSECO-Spider` folder using the `python -m pytest` command in the console.
