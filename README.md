# TrustSECO-Spider
This spider uses a combination of actual spidering (using BeautifulSoup) and API calls (using requests) in order to gather information from GitHub.

It uses GitHub's Device Flow in order to obtain a personal token, which then gets used for the API calls.

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

This project also contains a small demo file (demo.py) which can demo basic functionality. In order to use it, you have to specify which demo you would like to run by giving either of these command-line arguments:
- github -> will run a GitHub data-pull demo
- spider -> will run a BeautifulSoup spidering demo
- both   -> will run both demos