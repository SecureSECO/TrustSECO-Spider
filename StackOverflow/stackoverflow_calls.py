"""
File for looking at Stack Overflow code trends
"""
import requests


class StackOverflowCall:
    """Class methods for getting data from Stack Overflow"""

    def get_monthly_trends(self, package):
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

        # Devide the json into data and percentage data
        if 'Year' in response and 'Month' in response and 'TagPercents' in response:
            output = None

            if response['TagPercents'] is not None and package in response['TagPercents']:
                years = response['Year']
                months = response['Month']
                popularity = response['TagPercents'][package]

                # return list of date and percentage tuples.
                try:
                    output = list(zip(months, years, popularity, strict=True))
                except ValueError:
                    print('One of the zipped lists was not of the same length')

            return output
        else:
            print('Could not find the wanted data')
            return None
