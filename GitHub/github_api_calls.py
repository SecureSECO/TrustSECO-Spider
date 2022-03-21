# pylint: disable=C0200,C0301
"""
File for executing api calls to github
"""

import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

try:
    import github_constants as gc
except ImportError:
    import GitHub.github_constants as gc

"""doctsting"""
class GitHubAPICall:
    """
    Class methods for getting data from GitHub
    """

    def __init__(self):
        # Rate limit variables
        self.core_remaining   = 0
        self.search_remaining = 0
        self.rate_remaining   = 0

    def set_rate_limit_data(self):
        """
        Get the rate limit information from GitHub
        """

        # Get the rate limit information
        rate_limit_data = self.make_api_call(gc.BASE_URL_RATE, gc.RATE).json()
        self.core_remaining   = int(rate_limit_data['resources']['core']['remaining'])
        self.search_remaining = int(rate_limit_data['resources']['search']['remaining'])
        self.rate_remaining   = int(rate_limit_data['rate']['remaining'])

        # Tell the user how many API calls they have left
        print(f'Core rate-limit remaining: {self.core_remaining}')
        print(f'Search rate-limit remaining: {self.search_remaining}')
        print(f'Rate rate-limit remaining: {self.rate_remaining}')

    def get_all_data(self, owner, repo, version, year):
        """
        Returns all the data that this program can get from GitHub
        """

        # Get the individual data-points
        repository_data = self.get_basic_repository_data(owner, repo)
        version_data = self.get_version_data(owner, repo, version)
        owner_data = self.get_owner_data(owner)
        contributor_count = self.get_repository_contributor_count(owner, repo)
        #gitstar_ranking = self.get_gitstar_ranking(owner, repo, repository_data['language'], repository_data['stargazers_count'])
        yearly_commit_count = self.get_yearly_commit_count(owner, repo)
        commit_count_in_year = self.get_commit_count_in_year(owner, repo, year)
        total_download_count = self.get_total_download_count(owner, repo)
        version_download_count = self.get_version_download_count(owner, repo, version)
        zero_response_issues_count = self.get_zero_responses_issue_count(owner, repo)
        average_issue_resolution_time = self.get_average_issue_resolution_time(owner, repo)
        #version_issue_count = self.issue_count_per_version(owner, repo, version)

        # Return a JSON object containing all the data
        return {
            'repository_data': repository_data,
            'version_data': version_data,
            'owner_data': owner_data,
            'contributor_count': contributor_count,
            #'gitstar_ranking': gitstar_ranking,
            'yearly_commit_count': yearly_commit_count,
            'commit_count_in_year': commit_count_in_year,
            'total_download_count': total_download_count,
            'version_download_count': version_download_count,
            'zero_response_issues_count': zero_response_issues_count,
            'average_issue_resolution_time': average_issue_resolution_time,
            #'version_issue_count': version_issue_count
        }

    def get_basic_repository_data(self, owner, repo):
        """
        Get the basic information about the given repository
        """
        print('Getting repository data...')

        # Get the basic repository data
        repository_url = f'{gc.BASE_URL_REPOS}/{owner}/{repo}'
        repository_data = self.make_api_call(repository_url, gc.CORE)

        # Return the data
        return repository_data.json()

    def get_version_data(self, owner, repo, version):
        """
        Get information about a specific version/release of a repository
        """
        print('Getting version data...')

        # Get the basic repository data
        version_url = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/releases/tags/{version}'
        version_data = self.make_api_call(version_url, gc.CORE)

        # Return the data
        return version_data.json()

    def get_owner_data(self, owner):
        """
        Get the basic information about the repository owner
        """
        print('Getting owner data...')

        # Get owner data
        owner_url = f'{gc.BASE_URL_USERS}/{owner}'
        owner_data = self.make_api_call(owner_url, gc.CORE)

        # Return the data
        return owner_data.json()

    def get_repository_contributor_count(self, owner, repo):
        """
        Get the amount of contributors of the given repository
        """
        print('Getting contributor count...')

        # Get the contributors of the repository
        contributors_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/contributors?per_page=100&anon=1'
        contributors_data = self.make_api_call(contributors_url, gc.CORE)

        # Very simple error handling
        if contributors_data is None:
            print('Error occured while getting the contributor count.')
            return None

        # See if this repository has multiple pages of contributors
        if 'last' in contributors_data.links:
            # Get the amount of contributors on the final page
            final_page_data = self.make_api_call(contributors_data.links['last']['url'], gc.CORE)
            final_page_contributor_count = len(final_page_data.json())
            # Get the total page count
            page_count = int(contributors_data.links['last']['url'].split('=')[-1])
        else:
            # Get the amount of contributors on the first page
            final_page_contributor_count = len(contributors_data.json())
            # There is only one page
            page_count = 1

        # Return the total contributor count
        return (page_count - 1) * 100 + final_page_contributor_count

    def get_gitstar_ranking(self, owner, repo, language, star_count):
        """
        Get the GitStar ranking of the given repository
        If the repository is not ranked, return None
        Else, return the ranking
        """
        print('Getting GitStar ranking...')

        # Perform a basic search to list all the repositories in the given language, sorted by their stargazer count
        ranking_url  = f'{gc.BASE_URL_SEARCH}/repositories?q=stars:>0+language:{language}&sort=stars&order=desc&per_page=100'
        ranking_data = self.make_api_call(ranking_url, gc.SEARCH)

        # Very simple error handling
        if ranking_data is None:
            print('Error occured while getting the GitStar ranking.')
            return None

        # See if the result has multiple pages
        # If it does, perform a binary search to find the page with the given repository
        if 'last' in ranking_data.links:
            # Get the total amount of pages
            page_count = ranking_data.links['last']['url'].split('=')[-1]

            # Make sure that our repository's stargazer count is above the lowest query-able stargazer count
            final_page_data = self.make_api_call(ranking_data.links['last']['url'], gc.SEARCH)
            final_repo_star_count = final_page_data.json()['items'][-1]['stargazers_count']
            # If the our count is lower, return none
            if final_repo_star_count > star_count:
                return None

            # Perform binary searching to find the correct page
            lower_bound = 0
            upper_bound = int(page_count)
            base_url = ranking_url + '&page='
            while True:
                # Calculate the index of the middle page, and get the data from that page
                middle_page_number = int((upper_bound + lower_bound) / 2)
                ranking_url = base_url + str(middle_page_number)
                page_data = self.make_api_call(ranking_url, gc.SEARCH).json()

                # Get the highest and lowest stargazer counts from the query
                page_highest_star_count = page_data['items'][0]['stargazers_count']
                page_lowest_star_count = page_data['items'][-1]['stargazers_count']

                # See if the wanted stargazer count is within the bounds of the current page
                if page_highest_star_count >= star_count and page_lowest_star_count <= star_count:
                    # If so, find the repository in the page
                    for index in range(len(page_data['items'])):
                        if page_data['items'][index]['full_name'] == owner + '/' + repo:
                            return index + (middle_page_number - 1) * 100

                # If we didn't find the correct page, update the bounds
                if page_lowest_star_count > star_count:
                    lower_bound = middle_page_number
                elif page_highest_star_count < star_count:
                    upper_bound = middle_page_number

                # See if we have reached the end of the pages
                if upper_bound - lower_bound <= 1:
                    return None
        # Else, the repository should be on the first page
        else:
            # Find the repository in the page
            for current_repo in ranking_data.json()['items']:
                if current_repo['full_name'] == f'{owner}/{current_repo}':
                    return current_repo['stargazers_count']

            # If we didn't find the repository, return None
            return None

    def get_yearly_commit_count(self, owner, repo):
        """
        Get the amount of commits in the last year
        This 'last year' is counted from the current date
        """
        print('Getting yearly commit count...')

        # Get all the commits for the past year
        commits_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/stats/commit_activity'
        commits_data = self.make_api_call(commits_url, gc.CORE)

        # Very simple error handling
        if commits_data is None:
            print('Error occured while getting the yearly commit count.')
            return None

        # Sum all the weekly commit counts
        total_commits = 0
        for week in commits_data.json():
            total_commits += week['total']

        # Return the total commits
        return total_commits

    def get_commit_count_in_year(self, owner, repo, year):
        """
        Get the amount of commits in the given year
        """
        print(f'Getting commit count in year {year}...')

        # Get the commits for the given year
        commits_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/commits?per_page=100&since={year}-01-01T00:00:00Z&until={year}-12-31T23:59:59Z'
        commits_data = self.make_api_call(commits_url, gc.CORE)

        # Very simple error handling
        if commits_data is None:
            print(f'Error occured while getting the commit count in the year {year}.')
            return None

        # See if there are multiple pages of commits
        if 'last' in commits_data.links:
            # Get the amount of commits on the final page
            final_page_data = self.make_api_call(commits_data.links['last']['url'], gc.CORE)
            final_page_commit_count = len(final_page_data.json())
            # Get the total page count
            page_count = int(commits_data.links['last']['url'].split('=')[-1])
        else:
            # Get the amount of commits on the first page
            final_page_commit_count = len(commits_data.json())
            # There is only one page
            page_count = 1

        # Return the amount of commits
        return (page_count - 1) * 100 + final_page_commit_count

    def get_total_download_count(self, owner, repo):
        """
        Get the total amount of downloads of this repository
        """
        print('Getting total download count...')

        # Get the first page of releases
        releases_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/releases?per_page=100'
        releases_data = self.make_api_call(releases_url, gc.CORE)

        # Very simple error handling
        if releases_data is None:
            print('Error occured while getting the total download count.')
            return None

        # Get the total download count
        total_download_count = 0
        while True:
            # Add the download count of all the application assets for every release on this page
            for release in releases_data.json():
                for asset in release['assets']:
                    if 'application' in asset['content_type']:
                        total_download_count += asset['download_count']

            # See if we still have pages to go
            # If so, make an API call to the next page
            if 'next' in releases_data.links:
                releases_url = releases_data.links['next']['url'] + '&per_page=100'
                releases_data = self.make_api_call(releases_url, gc.CORE)
            # Else stop the loop, as we are done
            else:
                break

        # Return the total download count
        return total_download_count

    def get_version_download_count(self, owner, repo, version):
        """
        Get the total amount of downloads of a specific version
        """
        print(f'Getting download count of version {version}...')

        # Get the information for the given release
        version_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/releases/tags/{version}'
        version_data = self.make_api_call(version_url, gc.CORE)

        # Very simple error handling
        if version_data is None:
            print(f'Error occured while getting the download count of release {version}.')
            return None

        # Get the download count per non-text released asset
        total_version_download_count = 0
        for asset in version_data.json()['assets']:
            if 'application' in asset['content_type']:
                total_version_download_count += asset['download_count']

        # Return the total download count
        return total_version_download_count

    def get_zero_responses_issue_count(self, owner, repo):
        """
        Get the total amount of issues that have no responses
        """
        print('Getting zero-response issues count...')

        # Get the first page of issues
        issues_url = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/issues?per_page=100&state=open&sort=comments&direction=asc'
        issues_data = self.make_api_call(issues_url, gc.CORE)
        last_full_no_responses_page = 0

        # Very simple error handling
        if issues_data is None:
            print('Error occured while getting the 0-response-issues count.')
            return None

        while True:
            # See if there are more pages AND the last issue on this page has no responses
            # As if that is the case, we need to take a look a the next page
            if 'next' in issues_data.links and issues_data.json()[-1]['comments'] == 0:
                last_full_no_responses_page += 1
                issues_url = issues_data.links['next']['url'] + '&per_page=100&state=open&sort=comments&direction=asc'
                issues_data = self.make_api_call(issues_url, gc.CORE)
            # Else if there are no more pages, and the last issue on this page has no responses
            # Then this whole page must be full of 0-response issues, so return the total number of seen issues
            # We do last_full_no_responses_page + 1 because it refers to the previous page, and we need to add the current page to it
            elif issues_data.json()[-1]['comments'] == 0:
                return (last_full_no_responses_page + 1) * 100
            # Else, the final 0-responses issue must be somewhere within this page
            # So we need to find the index of it, and return it summed up with the total number of seen issues
            else:
                # Find the index of the final 0-responses issue
                last_no_response_index = 0
                for i in range(len(issues_data.json())):
                    if issues_data.json()[i]['comments'] == 0:
                        last_no_response_index = i
                    elif issues_data.json()[i]['comments'] > 0:
                        break

                # Return the total number of seen issues + the index of the last 0-response issue
                return (last_full_no_responses_page * 100) + last_no_response_index

    def get_average_issue_resolution_time(self, owner, repo):
        """
        Get the average resolution time of the last 200 issues
        Returns the average resolution time in seconds
        """
        print('Getting average issue resolution time...')

        # Get the first page of closed issues
        issue_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/issues?per_page=100&state=closed&sort=created&direction=desc'
        issue_data = self.make_api_call(issue_url, gc.CORE)

        # Very simple error handling
        if issue_data is None:
            print('Error occured while getting the average issue resolution time.')
            return None

        # Add the issues of the first page to the JSON object
        all_issues = issue_data.json()

        # If there are more pages, add the next 100 issues to the JSON object as well
        # For now, we only use a maximum of 200 issues, as otherwise we would be making too many API calls
        if 'next' in issue_data.links:
            issue_url  = issue_data.links['next']['url'] + '&per_page=100&state=closed&sort=created&direction=desc'
            issue_data = self.make_api_call(issue_url, gc.CORE)
            all_issues += issue_data.json()

        # Variable to store the total resolution time in seconds
        total_resolution_time = 0

        # Loop through all the issues, and add up the time between the issue creation and the issue resolution
        for issue in all_issues:
            # Calculate the resolution time
            creation_date = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            closure_date  = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
            issue_resolution_time = closure_date - creation_date

            # Add the resolution time to the total
            total_resolution_time += issue_resolution_time.seconds

        # Return the average resolution time
        return total_resolution_time / len(all_issues)

    def issue_count_per_version(self, owner, repo, version):
        """
        Get the publish date of the given version
        and the version after it (if it exists)

        Then perform a search API call to find all issues that were posted between those dates
        """
        print(f'Getting issue count for version {version}...')

        # Get the publish dates of the given version and the version after it
        (given_version_date, next_version_date) = self.get_version_dates(owner, repo, version)

        if next_version_date is None:
            # Get the total amount of issues that were posted between those dates
            issues_url  = f'{gc.BASE_URL_SEARCH}/issues?q=is:issue+created:{given_version_date}..*+repo:{owner}/{repo}&per_page=100'
            issues_data = self.make_api_call(issues_url, gc.SEARCH)
            issue_count = issues_data.json()['total_count']
        else:
            # Get the total amount of issues that were posted between those dates
            issues_url  = f'{gc.BASE_URL_SEARCH}/issues?q=is:issue+created:{given_version_date}..{next_version_date}+repo:{owner}/{repo}&per_page=100'
            issues_data = self.make_api_call(issues_url, gc.SEARCH)
            issue_count = issues_data.json()['total_count']

        # Return this count
        return issue_count

    def get_version_dates(self, owner, repo, version):
        """
        Get the publish date of the given version and the version after it (if it exists)
        Presumes that the repository
        """

        # Get the information about the first releases
        releases_url  = f'{gc.BASE_URL_REPOS}/{owner}/{repo}/releases?per_page=100'
        releases_data = self.make_api_call(releases_url, gc.CORE)
        previous_page = None

        while True:
            # Get the json data for easy access
            releases_json = releases_data.json()

            # See if the current version is within the current page
            for i in range(len(releases_json)):
                # If it is, and there is an entry before the current one (aka later in time)
                # Return the publish dates of both
                if releases_json[i]['tag_name'] == version and i > 0:
                    return (releases_json[i]['published_at'], releases_json[i - 1]['published_at'])

                # If it is and there is no entry before the current one, but we have a previous page
                # Return the publish date of the current previous version on the previous page
                if releases_json[i]['tag_name'] == version and i == 0:
                    # If there is no previous page, return None for the previous version
                    if previous_page is None:
                        return (releases_json[i]['published_at'], None)

                    # Else return the publish date of the previous version
                    return (releases_json[i]['published_at'], previous_page.json()[-1]['published_at'])

            # If there is a next page, update previous_page and releases_data
            if 'next' in releases_data.links:
                # If the current version is not within the current page, check the next page
                previous_page = releases_data
                # Update releases_data by making a new API call to the given next page
                releases_url  = releases_data.links['next']['url'] + '&per_page=100'
                releases_data = self.make_api_call(releases_url, gc.CORE)
            # Else, there are no more pages, so return None for both dates
            else:
                return (None, None)

    def get_owner_stargazer_count(self, owner):
        """
        Get the stargazer count of the given owner

        Can take a lot of API calls and time, as an owner can have a lot of repositories
        """
        print(f'Getting stargazer count for owner {owner}...')

        # Get the stargazer count
        stargazer_url  = f'{gc.BASE_URL_ORGS}/{owner}/repos?per_page=100'
        stargazer_data = self.make_api_call(stargazer_url, gc.CORE)

        total_stargazer_count = 0

        while True:
            # Loop through all the repositories of the owner
            for repo in stargazer_data.json():
                # Add the stargazer count of the current repository to the total
                total_stargazer_count += repo['stargazers_count']

            # If there is a next page, update stargazer_data
            if 'next' in stargazer_data.links:
                # Update stargazer_data by making a new API call to the given next page
                stargazer_url  = stargazer_data.links['next']['url'] + '&per_page=100'
                stargazer_data = self.make_api_call(stargazer_url, gc.CORE)
            # Else, there are no more pages, so return the total stargazer count
            else:
                return total_stargazer_count

    def make_api_call(self, api_url, call_type, given_headers = None):
        """
        Perform a simple GET request, based off the given URL
        """

        # Ignore these checks if the call_type is RATE
        if not call_type == gc.RATE:
            if self.search_remaining == 0 or self.core_remaining == 0:
                print('Fetching new rate limit data...')
                self.set_rate_limit_data()

            # See if the user has search API calls left
            # If not, return None
            if call_type == 'search' and self.search_remaining == 0:
                print('Search limit reached.')
                return None

            # See if the user has core API calls left
            # If not, return None
            if call_type == 'core' and self.core_remaining == 0:
                print('Core limit reached.')
                return None

        # Define the header
        headers = {'Authorization': 'token ' + os.getenv('GITHUB_TOKEN'),
                   'Accept': 'application/vnd.github.v3+json'}

        # Add the given headers, if any
        if not given_headers is None:
            headers.update(given_headers)

        # Basic request to get the information.
        data_response = requests.get(api_url,headers=headers)

        # See if we got a valid response
        if data_response.status_code == 200:
            data = data_response

            # Decrement the appropriate rate limit variable
            if call_type == 'search':
                self.search_remaining -= 1
            elif call_type == 'core':
                self.core_remaining -= 1
            elif call_type == 'rate':
                self.rate_remaining -= 1
        else:
            print('Unable to get data from GitHub')
            print(f'Error: {data_response.status_code}')
            data = None
            
        return data


#example test function for github actions
def addOne(arg):
    return arg+1
