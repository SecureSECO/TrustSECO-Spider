"""
File for looking at Stack Overflow code trends
"""
import requests


class StackOverflowCall:
    """Class methods for getting data from Stack Overflow"""

    def get_Monthly_Trends(self, language):
        """
        Gets popularity of a language each month since 2008
        """

        # Take the url for Stack Overflow trends
        url = "https://insights.stackoverflow.com/trends/get-data"

        # Extract the data as json
        response = requests.get(url).json()

        # Devide the json into data and percentage data
        years = response.get("Year")
        months = response.get("Month")
        popularity = response.get("TagPercents").get(language)

        # return list of date and percentage tuples.
        return list(zip(months, years, popularity, strict=True))
