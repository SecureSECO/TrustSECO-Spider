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

        url = "https://insights.stackoverflow.com/trends/get-data"
        response = requests.get(url)
        years = response.json().get("Year")
        months = response.json().get("Month")
        popularity = response.json().get("TagPercents").get(language)

        print("The language {0} was used by {1} percent of users in {2} {3}",
              language, popularity[1], months[1], years[1])
