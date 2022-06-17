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

    def get_monthly_popularity(self, package: str) -> dict:
        """
        Get the monthly popularity of the given package.

        Parameters:
            package (str): The name of the package

        Returns:
            Tuple: The monthly popularity of the given package

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
        if 'Year' in response and 'Month' in response and 'TagPercents' in response:
            # Make sure that the percentages have actual values
            if response['TagPercents'] is not None:
                # See if the package is present in the response
                # If so, return the latest popularity data
                if package in response['TagPercents']:
                    years = response['Year']
                    months = response['Month']
                    popularity = response['TagPercents'][package]

                    # Return the latest popularity with the corresponding year and month
                    try:
                        latest_data = list(
                            zip(months, years, popularity, strict=True))[-1]

                        return {
                            "month": latest_data[0],
                            "year": latest_data[1],
                            "popularity": latest_data[2]
                        }
                    except ValueError as e:
                        logging.error(
                            'Monthly popularity: One of the lists was not of the same length')
                        logging.error(e)
                        return None
                else:
                    logging.info('Package not in response')

                    return {
                        "month": response['Month'][-1],
                        "year": response['Year'][-1],
                        "popularity": 0
                    }

        logging.warning(
            'Monthly popularity: Did not get valid response (missing data)')
        return None


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
