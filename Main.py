"""
Basic main file, purely for demonstration purposes.
"""

import os
import os.path
import json
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from dotenv import load_dotenv
from GitHub.github_api_calls import GitHubAPICall
from GitHub.github_get_token import authenticate_user
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
    """

    runner = CrawlerRunner()
    results = {}
    runner.crawl(GitHubUsers,      'numpy', 'numpy', results)
    runner.crawl(GitHubIssueRatio, 'numpy', 'numpy', results)
    temp = runner.join()
    temp.addBoth(lambda _: reactor.stop())
    reactor.run()
    print(results)

#github_demo()
scrapy_demo()
