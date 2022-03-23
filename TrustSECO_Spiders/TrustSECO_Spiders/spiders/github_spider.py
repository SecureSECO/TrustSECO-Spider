# pylint: disable=W0221
"""
The implementation of the spider for crawling Github.
"""

import logging
import scrapy

class GitHubUsers(scrapy.Spider):
    """
    Gets the number of users of the repository
    """

    name = 'github_users'
    allowed_domains = ['github.com']
    start_urls = []

    def __init__(self, owner, repo, results, *args, **kwargs):
        # Global variable so we can get back the results
        self.items = results

        # Set the urls
        self.start_urls.append(f'https://github.com/{owner}/{repo}')

        # Disabling the default logging
        logging.getLogger('scrapy').setLevel(logging.ERROR)
        logging.getLogger('filelock').setLevel(logging.ERROR)

        # Initializing the spider
        super().__init__(*args, **kwargs)

    def parse(self, response):
        """
        Get the amount of users

        This number is available in an <span> tag within an <a> tag.
        Hence, we search for the <a> tags first, as that contains the text "Used by"
        which we will use to identify which <span> tag we need to get the number from.
        """

        # Get the appropriate <a> tags that might contain our number
        possible_links = response.css('a.Link--primary.no-underline')

        # Initialise the counter to None
        user_count = None

        # Go through all the <a> tags and find the one containing "Used by"
        # as this is the one containing the number of users
        for link in possible_links:
            if 'Used by' in link.css('::text').extract_first():
                value = link.css('span.Counter::attr(title)').extract_first()
                if value is not None:
                    user_count = value
                    break

        # Update the items dictionary so we can use the result
        self.items.update({'users':user_count})

        # Yield the items as per regular spider conventions
        yield self.items

class GitHubIssueRatio(scrapy.Spider):
    """
    Gets the ratio of open to closed issues of the repository
    """

    name = 'github_issue_ratio'
    allowed_domains = ['github.com']
    start_urls = []

    def __init__(self, owner, repo, results, *args, **kwargs):
        # Global variable so we can get back the results
        self.items = results

        # Set the urls
        self.start_urls.append(f'https://github.com/{owner}/{repo}/issues')

        # Disabling the default logging
        logging.getLogger('scrapy').setLevel(logging.ERROR)
        logging.getLogger('filelock').setLevel(logging.ERROR)

        # Initializing the spider
        super().__init__(*args, **kwargs)

    def parse(self, response):
        """
        Get the open to closed issues ratio

        The number of open/closed issues can be found on the '/issues' page.
        Both numbers are contained in an <a> tag.
        """

        # Get all the text elements within the appropriate <a> tags
        possible_links = response.css('a.btn-link::text').getall()

        # Try to find the open/closed issues count
        open_issues = None
        closed_issues = None
        for value in possible_links:
            # Parse the string to get the actual number
            # The string looks like '\n      x ___issues    \n'
            # So, we remove the newline chars and strip it to get rid of the whitespace
            # Then, we split on ' ' to get [x, '___issues'], of which we get the first element
            actual_value = value.replace('\n', '').replace(',', '').strip().split(' ')[0]

            # Set the open/closed issues count
            if 'Open' in value:
                open_issues = int(actual_value)
            elif 'Closed' in value:
                closed_issues = int(actual_value)

        # If we weren't able to find both counts, then return None
        if open_issues is None or closed_issues is None:
            self.items.update({'issue_ratio':None})
        # Else, calculate the ratio and return it
        else:
            self.items.update({'issue_ratio':open_issues/closed_issues})

        # Yield the items as per regular spider conventions
        yield self.items
