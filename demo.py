"""
Basic demo file, purely for demonstration purposes.

Allows the user to test the Device Flow authentication process,
GitHub API calls, and spidering.
"""

# For json converting
import json
# For accessing the GitHub data-points
import interface


def github_demo():
    """
    Basic retrieval method of github data.
    This function currently gets every bit of data we can
    But this can obviously be reduced to a specific data-point
    """

    # Get the data
    data = interface.get_repository_language('numpy', 'numpy')

    # Print the json data in a readable way
    print(json.dumps(data, indent=4))


def broken_scrapy_demo():
    """
    Basic demo of scraping data from github.

    Due to the nature of a spider (it being able to only scrape a single page type),
    we have to create a new spider for each trust fact.

    At the moment we can request the following data:
    - User count
    - Issue Ratio
    """

    # Add the wanted spiders to the runner
    user_count = interface.get_repository_user_count('numpy', 'numpy')
    print('User count: ' + str(user_count))
    issue_ratio = interface.get_repository_issue_ratio('numpy', 'numpy')
    print('Issue ratio: ' + str(issue_ratio))


def working_scrapy_demo():
    from scrapy.crawler import CrawlerRunner
    from TrustSECO_Spiders.TrustSECO_Spiders.spiders.github_spider import GitHubUsers, GitHubIssueRatio
    from twisted.internet import reactor

    runner = CrawlerRunner()
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


# ithub_demo()


# scrapy_demo()


working_scrapy_demo()
