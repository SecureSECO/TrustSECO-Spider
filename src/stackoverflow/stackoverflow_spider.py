"""File containing the Stack Overflow spider

This file contains the logic for the spider that will
allow the program to use BeautifulSoup and Requests
in order to scrape wanted data-points from the Stack Overflow website.

    Typical usage:

    foo = StackOverflowSpider()
    bar = foo.get_monthly_popularity('package')
"""

# Import for improved logging
import logging
# Import for sending and handling HTTP requests
import requests


class StackOverflowSpider:
    """Class methods for getting data from Stack Overflow

    This class handles all of the spidering jobs for the Stack Overflow website.
    It uses requests to get the webpage, and BeautifulSoup to parse and traverse it.
    """

    def get_monthly_popularity(self, package: str) -> float:
        """
        Get the monthly popularity of the given package.

        Args:
            package (str): The name of the package

        Returns:
            float: The latest monthly popularity of the given package

            This popularity is the percentage of questions posted that were about the given package.
        """

        logging.info('Getting monthly popularity')

        # Take the url for Stack Overflow trends
        url = 'https://insights.stackoverflow.com/trends/get-data'

        # Extract the data as json
        try:
            response = requests.get(url).json()
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return None

        # Make sure we got the correct data
        if 'TagPercents' not in response:
            logging.error('Could not find TagPercents in response')
            return None

        # Make sure we got the correct data
        if response['TagPercents'] is None:
            logging.error('TagPercents is None')
            return None

        # Make sure that the package is in the response
        if package not in response['TagPercents']:
            logging.warning('Package not found in response')
            return 0

        # Return the latest monthly popularity of the given package
        return response['TagPercents'][package][-1]


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
