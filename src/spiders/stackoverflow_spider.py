"""File containing the Stack Overflow spider

This file contains the logic for the spider that will
allow the program to use BeautifulSoup and Requests
in order to scrape wanted data-points from the Stack Overflow website.

    Typical usage:

    foo = StackOverflowSpider()
    bar = foo.get_monthly_popularity('package')
"""

import requests


class StackOverflowSpider:
    """Class methods for getting data from Stack Overflow

    This class handles all of the spidering jobs for the Stack Overflow website.
    It uses requests to get the webpage, and BeautifulSoup to parse and traverse it.
    """

    def get_monthly_popularity(self, package) -> int:
        """
        Get the monthly popularity of the given package.

        Parameters:
            package (str): The name of the package

        Returns:
            int: The monthly popularity of the given package

            This popularity is the percentage of questions posted that were about the given package.
        """

        # Take the url for Stack Overflow trends
        url = 'https://insights.stackoverflow.com/trends/get-data'

        # Extract the data as json
        try:
            response = requests.get(url).json()
        except requests.exceptions.RequestException as e:
            print('Error:', e)
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
                        return list(zip(months, years, popularity, strict=True))[-1]
                    except ValueError:
                        print('One of the lists was not of the same length')
                        return None
                else:
                    print('Package not in response')
                    return (response['Month'][-1], response['Year'][-1], 0)

        print('Did not get valid response')
        return None


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
