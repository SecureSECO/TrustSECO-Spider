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


def scrapy_demo():
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


github_demo()
scrapy_demo()
