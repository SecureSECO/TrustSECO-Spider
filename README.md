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
As a fair amount of library imports are needed for this project, we have included a PIP compatible requirements file which can be used to automatically download all the needed packages. Simply use the command ```pip install -r requirements.txt```.

### Demo
This project also contains a small demo file (demo.py) which can demo basic functionality. Simply enter ```python .\demo.py``` in the command line in order to get a list of possible arguments. With these arguments you can specify which of the demos to run, and if you want to include GitHub SEARCH API calls. The SEARCH API calls are seperated on purpose, as it has a rather low rate limit, and we don't want to exceed that just due to running the demo a few times.

Depending on the given arguments, the demo will grab all of the available GitHub and Libraries.io data-points, and print them to the console.
Example commands:
- ```python .\demo.py numpy```          -> Gets all the data-points for the numpy package/repository (besides the SEARCH API points)
- ```python .\demo.py all gh_search```  -> Gets all the data-points for both numpy and AFNetworking, and includes the SEARCH API points

### Unit tests
The project also contains some of the unit tests too. These can be started from within the main ```TrustSECO-Spider``` folder using the ```python -m pytest``` command in the console.