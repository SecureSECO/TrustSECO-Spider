# TrustSECO-Spider

This spider uses a combination of actual spidering (using BeautifulSoup) and API calls (using requests) in order to gather information from GitHub and Libraries.io.

## GitHub

Our program uses GitHub's Device Flow in order to obtain a personal token, which then gets used for the API calls.

It retrieves most data-points using GitHub's REST API. Sadly, not all of the wanted data-points were accessible this way. In order to still gather this data, spidering had to be used.

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

As Libraries.io does not have a 'Device Flow' like way to obtain a personal token, the user will have to enter this manually when starting the program.

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

## How to use

### Requirements

This package is initialized as an npm package so it can be easily imported in node projects. However the functionality is written in python. You can find all the python files in the src folder. When installing the python depenencies, it is important that the path given to `pynode.appendSysPath()` in `index.js` line 4 is set to the place where the packages are actually installed.

The standard path we use is `src/env/Lib/site-packages`.
If you want to install python packages in an virtual environment on the same location follow these steps:

0. Make sure python3 installed on your machine
1. Navigate to the `src` folder within the TRUSTSECO-SPIDER directory in a command terminal.
2. Create a virtual environment by running the command: `python -m venv env`
3. Navigate into the `env/Scripts` folder.
4. Activate the venv by running the `activate.bat` exacutable.
5. You should now see this: `(env) C:/Users/<yourusername>/Documents/TrustSECO-Spider/src/env/Scripts>`
6. Navigate back to the `src` folder
7. Install packages in env with pip running: `pip install -r requirements.txt`

### Demo

This project also contains a small demo file (demo.py) which can demo basic functionality. Simply enter `python .\demo.py` in the command line in order to get a list of possible arguments. With these arguments you can specify which of the demos to run.

Depending on the given arguments, the demo will grab all of the available GitHub and Libraries.io data-points, and print them to the console.
Current commands:

- `python .\demo.py numpy` -> Gets all the data-points for the numpy package/repository
- `python .\demo.py afnetworking` -> Gets all the data-points for the AFNetworking package/repository
- `python .\demo.py all` -> Gets all the data-points for both numpy and AFNetworking

### Unit tests

The project also contains some of the unit tests too. These can be started from within the main `TrustSECO-Spider` folder using the `python -m pytest` command in the console.
