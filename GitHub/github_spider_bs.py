"""
Allow the program to use BeautifulSoup and Requests in order to
scrape wanted data-points from the GitHub website.
"""

from bs4 import BeautifulSoup
import requests


def get_repository_user_count(owner, repo):
    """
    Gets the number of users of a given repository
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
    possible_links = soup.find_all('a', class_='Link--primary no-underline')

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


def get_repository_issue_ratio(owner, repo):
    """
    Gets the issue ratio of a given repository
    """

    # Create the URL for the repository
    issues_page_url = f'https://github.com/{owner}/{repo}/issues'

    # Get the issues page
    issues_page = requests.get(issues_page_url)

    # Make sure the main page is valid
    if issues_page.status_code != 200:
        return None

    # Create a BeautifulSoup object
    soup = BeautifulSoup(issues_page.text, 'html.parser')

    # Get the <a> tags that might contain our numbers
    possible_links = soup.find_all('a', class_='btn-link')

    # Try to find the open/closed issues count
    open_issues = None
    closed_issues = None
    # Go through all the <a> tags and find the ones containing "open" and "closed"
    # as these are the ones containing the number of issues
    for link in possible_links:
        if 'open' in link.text.lower():
            value = link.text.replace(',', '').replace('\n', '').strip()
            open_issues = int(value.split(' ')[0])
        elif 'closed' in link.text.lower():
            value = link.text.replace(',', '').replace('\n', '').strip()
            closed_issues = int(value.split(' ')[0])

        # Break if we have found both numbers
        if open_issues is not None and closed_issues is not None:
            break

    # If we found both numbers, return the ratio
    if open_issues is not None and closed_issues is not None and closed_issues != 0:
        return open_issues / closed_issues
    # Else return None
    return None
