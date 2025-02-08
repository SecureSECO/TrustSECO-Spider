"""File containing the GitHub spider

This file contains the logic for crawling through the [GitHub website](https://github.com/).

This crawling is done by using the [Requests](https://requests.readthedocs.io/en/latest/) library for HTTP calls,
and the [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library for HTML parsing.

Only the data-points that the API endpoints cannot provide are spidered.
"""

# Import for sending and handling HTTP requests
import requests
# Import for parsing and searching through HTML
from bs4 import BeautifulSoup


class GitHubSpider:
    """Class containing the GitHub spider"""

    def get_repository_user_count(self, owner: str, repo: str) -> int | None:
        """Function to get the number of users of a given repository.

        To do this we simply look through the repository page and find
        the "used by" section.

        Args:
            owner (str): The owner of the repository.
            repo (str): The repository.

        Returns:
            int: The number of users of the repository.
        """

        # Create the URL for the repository
        main_page_url = f'https://github.com/{owner}/{repo}'

        # Get the main page
        main_page = requests.get(main_page_url)

        # Make sure the main page is valid
        if main_page.status_code != 200:
            return None

        # Create a BeautifulSoup object
        soup = BeautifulSoup(main_page.text, 'html.parser')

        # Get the <a> tags that might contain our number
        possible_links = soup.find_all(
            'a', class_='Link--primary no-underline Link')

        # Initialise the counter to None
        user_count = None
        # Go through all the <a> tags and find the one containing "Used by"
        # as this is the one containing the number of users
        for link in possible_links:
            if 'used by' in link.text.lower():
                value = link.span.get('title')
                if value is not None:
                    # Remove unwanted characters
                    value = value.replace(',', '').replace('\n', '').strip()
                    # Convert to integer
                    user_count = int(value.split(' ')[0])
                    # Break as we have found our wanted node
                    break

        return user_count

"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
