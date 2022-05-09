"""
File for looking at Stack Overflow code trends
"""
import requests


class StackOverflowSpider:
    """Class methods for getting data from Stack Overflow"""

    def get_monthly_popularity(self, package):
        """
        Gets popularity list of a package on Stack Overflow in percentage from each month since 2008
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
