"""
Basic main file, purely for demonstration purposes.
"""

# For file interaction
import os
import os.path
# For json converting
import json
# For the spidering
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
# For local environmental variable usage
from dotenv import load_dotenv
# Authenticating the user via GitHub
from GitHub.github_get_token import authenticate_user
# For accessing the GitHub data-points
# API
from GitHub.github_api_calls import GitHubAPICall
# Spider
from TrustSECO_Spiders.TrustSECO_Spiders.spiders.github_spider import GitHubUsers, GitHubIssueRatio

# Make sure that the .env file exists
if not os.path.exists('.env'):
    with open('.env', 'wt', encoding='utf-8') as env_file:
        pass

# Load the .env file
load_dotenv()

def github_demo():
    """
    Basic retrieval method of github data.
    This function currently gets every bit of data we can
    But this can obviously be reduced to a specific data-point
    """
    # Authenticate the user if needed
    if os.getenv('GITHUB_TOKEN') is None:
        print("No GitHub token found. Authenticating user...")

        # Authenticate the user
        authenticate_user('1c3bf96ae6a2ec75435c')
    else:
        print("GitHub token found. Getting data...")

    # Create an API call object
    github = GitHubAPICall()

    # Get the data
    all_data = github.get_all_data(
        # Owner
        'numpy',
        # Repository
        'numpy',
        # Version
        'v1.22.3',
        # Commit year
        2021
        )

    # Print the json data in a readable way
    print(json.dumps(all_data, indent=4))

def scrapy_demo():
    """
    Basic demo of scraping data from github.

    Due to the nature of a spider (it being able to only scrape a single page type),
    we have to create a new spider for each trust fact.

    At the moment we can request the following data:
    - User count
    - Issue Ratio
    """

    # Dictionary in which the spiders will store the results
    results = {}

    # Create a crawler runner which helps running multiple spiders at once
    runner = CrawlerRunner()
    # Add the wanted spiders to the runner
    runner.crawl(GitHubUsers,      'numpy', 'numpy', results)
    runner.crawl(GitHubIssueRatio, 'numpy', 'numpy', results)
    # Join the requests and make sure they stop the Twisted Reactor when they are done
    temp = runner.join()
    temp.addBoth(lambda _: reactor.stop())
    # Start the spidering process
    # This function will block untill all the spiders are done
    reactor.run()

    # Print the results
    print(results)

#github_demo()
scrapy_demo()
