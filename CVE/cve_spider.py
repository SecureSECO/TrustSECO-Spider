"""
Allow the program to use BeautifulSoup and Requests in order to
scrape wanted data-points from the CVE website.
"""

import datetime
import requests
from bs4 import BeautifulSoup


class CVESpider:
    """
    Class methods for getting data from the CVE website using BeautifulSoup and requests for spidering
    """

    def get_cve_vulnerability_count(self, name):
        """
        Gets the amount of known vulnerabilities of a given package
        """

        # Get the list of CVE links
        links = self.get_cve_links(name)

        # Return the list of CVE data
        return len(links)

    def get_all_cve_data(self, name):
        """
        Loops through all the found CVE vulnerabilities, and extracts the data
        """

        # Get the list of CVE links
        links = self.get_cve_links(name)

        # Initialise the list of CVE data
        data = []
        # Go through all the links and extract the CVE data
        for link in links:
            data.append(self.extract_cve_data(link.get('href')))

        # Return the list of CVE data
        return data

    def get_cve_links(self, name):
        """
        Returns a list of links that refer to known vulnerabilities for the given package
        """

        # Make a GET request to the CVE website with the given package name
        html = requests.get(
            f'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={name}')
        # Convert the raw HTML into a BeautifulSoup object
        soup = BeautifulSoup(html.text, 'html.parser')

        # Find the <a> tags that contain the CVE links
        table = soup.find_all('table')[2]
        links = table.find_all('a')

        # Return the list of CVE links
        return links

    def extract_cve_data(self, cve_link):
        """
        Extracts the data from a given CVE link
        """

        # Create the URL, and make a GET request to the CVE website
        full_url = f'https://cve.mitre.org/{cve_link}'
        html = requests.get(full_url)
        # Convert the raw HTML into a BeautifulSoup object
        soup = BeautifulSoup(html.text, 'html.parser')

        # Extract the data from the CVE webpage
        cve_data = {
            'CVE_ID': soup.find_all('h2')[0].text,
            'CVE_vulnerability_description': soup.find_all('td')[10].text.strip(),
            'record_date': datetime.datetime.strptime(soup.find_all('b')[1].text, '%Y%m%d'),
            'CVE_link': full_url
        }

        # Return the CVE data
        return cve_data
