"""
File for executing api calls to github
"""

from datetime import datetime
import constants
from api_calls.api_calls import make_api_call


class GitHubAPICall:
    """Class methods for getting data from GitHub"""

    def __init__(self):
        # Rate limit variables
        self.core_remaining = 0
        self.search_remaining = 0

    def get_basic_repository_data(self, owner, repo):
        """
        Get the basic information about the given repository
        """
        print('Getting repository data...')

        # Get the basic repository data
        repository_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}'
        repository_data = self.try_perform_api_call(
            repository_url, constants.CORE)

        # Return the data, if it exists
        if repository_data is not None:
            return repository_data.json()
        else:
            print('Error occured while getting the repository data.')
            return None

    def get_repository_language(self, owner, repo):
        """
        Get the language of the given repository
        """
        print('Getting repository language...')

        # Get the basic repository data
        repository_data = self.get_basic_repository_data(owner, repo)

        # Return the data, if it exists
        if repository_data is not None and 'language' in repository_data:
            return repository_data['language']
        else:
            print('Error occured while getting the repository language.')
            return None

    def get_repository_stargazer_count(self, owner, repo):
        """
        Get the stargazer count of the given repository
        """
        print('Getting repository stargazer count...')

        # Get the basic repository data
        repository_data = self.get_basic_repository_data(owner, repo)

        # Return the data, if it exists
        if repository_data is not None and 'stargazers_count' in repository_data:
            return repository_data['stargazers_count']
        else:
            print('Error occured while getting the repository stargazer count.')
            return None

    def get_release_data(self, owner, repo, release):
        """
        Get information about a specific release/release of a repository
        """
        print('Getting release data...')

        # Get the basic repository data
        release_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/releases/tags/{release}'
        release_data = self.try_perform_api_call(release_url, constants.CORE)

        # Return the data, if it exists
        if release_data is not None:
            return release_data.json()
        else:
            print('Error occured while getting the release data.')
            return None

    def get_owner_data(self, owner):
        """
        Get the basic information about the repository owner
        """
        print('Getting owner data...')

        # Get owner data
        owner_url = f'{constants.BASE_URL_USERS}/{owner}'
        owner_data = self.try_perform_api_call(owner_url, constants.CORE)

        # Return the data, if it exists
        if owner_data is not None:
            return owner_data.json()
        else:
            print('Error occured while getting the owner data.')
            return None

    def get_repository_contributor_count(self, owner, repo):
        """
        Get the amount of contributors of the given repository
        """
        print('Getting contributor count...')

        # Get the contributors of the repository
        contributors_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/contributors?per_page=100&anon=1'
        contributors_data = self.try_perform_api_call(
            contributors_url, constants.CORE)

        # Very simple error handling
        if contributors_data is None:
            print('Error occured while getting the contributor count.')
            return None

        # See if this repository has multiple pages of contributors
        if 'last' in contributors_data.links:
            # Get the amount of contributors on the final page
            final_page_data = self.try_perform_api_call(
                contributors_data.links['last']['url'], constants.CORE)

            # Make sure we got a valid response
            if final_page_data is None:
                print('Error occured while getting the final contributor page.')
                return None

            final_page_contributor_count = len(final_page_data.json())
            # Get the total page count
            page_count = int(
                contributors_data.links['last']['url'].split('=')[-1])
        else:
            # Get the amount of contributors on the first page
            final_page_contributor_count = len(contributors_data.json())
            # There is only one page
            page_count = 1

        # Return the total contributor count
        return (page_count - 1) * 100 + final_page_contributor_count

    def get_gitstar_ranking(self, owner, repo):
        """
        Get the GitStar ranking of the given repository
        If the repository is not ranked, return None
        Else, return the ranking
        """
        print('Getting GitStar ranking...')

        # Get the needed extra information
        repo_data = self.get_basic_repository_data(owner, repo)

        # Make sure we got a valid response
        if repo_data is None:
            return None

        # Get the language of the repository
        language = repo_data['language']
        # Get the stargazer count of the repository
        stargazer_count = repo_data['stargazers_count']

        # Perform a basic search to list all the repositories in the given language, sorted by their stargazer count
        ranking_url = f'{constants.BASE_URL_SEARCH}/repositories?q=stars:>0+language:{language}&sort=stars&order=desc&per_page=100'
        ranking_data = self.try_perform_api_call(ranking_url, constants.SEARCH)

        # Make sure we got a valid response
        if ranking_data is None:
            print('Error occured while getting the GitStar ranking.')
            return None

        # See if the result has multiple pages
        # If it does, perform a binary search to find the page with the given repository
        if 'last' in ranking_data.links:
            # Get the total amount of pages
            page_count = ranking_data.links['last']['url'].split('=')[-1]

            # Make sure that our repository's stargazer count is above the lowest query-able stargazer count
            final_page_data = self.try_perform_api_call(
                ranking_data.links['last']['url'], constants.SEARCH)

            # Make sure we got a valid response
            if final_page_data is None:
                print('Error occured while getting the final ranking page.')
                return None

            # Get the stargazer count of the lsat entry on the last page
            final_repo_star_count = final_page_data.json()[
                'items'][-1]['stargazers_count']
            # If the our count is lower, return none
            if final_repo_star_count > stargazer_count:
                return None

            # Perform binary searching to find the correct page
            lower_bound = 0
            upper_bound = int(page_count)
            base_url = ranking_url + '&page='
            while True:
                # Calculate the index of the middle page, and get the data from that page
                middle_page_number = int((upper_bound + lower_bound) / 2)
                ranking_url = base_url + str(middle_page_number)
                page_data_response = self.try_perform_api_call(
                    ranking_url, constants.SEARCH)

                # Make sure we got a valid response
                if page_data_response is None:
                    print('Error occured while getting the ranking page.')
                    return None

                # Get the JSON information out of the response
                page_data = page_data_response.json()

                # Get the highest and lowest stargazer counts from the query
                page_highest_star_count = page_data['items'][0]['stargazers_count']
                page_lowest_star_count = page_data['items'][-1]['stargazers_count']

                # See if the wanted stargazer count is within the bounds of the current page
                if page_highest_star_count >= stargazer_count and page_lowest_star_count <= stargazer_count:
                    # If so, find the repository in the page
                    for index in range(len(page_data['items'])):
                        if page_data['items'][index]['full_name'] == owner + '/' + repo:
                            return index + (middle_page_number - 1) * 100

                # If we didn't find the correct page, update the bounds
                if page_lowest_star_count > stargazer_count:
                    lower_bound = middle_page_number
                elif page_highest_star_count < stargazer_count:
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
        commits_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/stats/commit_activity'
        commits_data = self.try_perform_api_call(commits_url, constants.CORE)

        # Make sure we got a valid response
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
        commits_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/commits?per_page=100&since={year}-01-01T00:00:00Z&until={year}-12-31T23:59:59Z'
        commits_data = self.try_perform_api_call(commits_url, constants.CORE)

        # Make sure we got a valid response
        if commits_data is None:
            print(
                f'Error occured while getting the commit count in the year {year}.')
            return None

        # See if there are multiple pages of commits
        if 'last' in commits_data.links:
            # Get the amount of commits on the final page
            final_page_data = self.try_perform_api_call(
                commits_data.links['last']['url'], constants.CORE)

            # Make sure we got a valid response
            if final_page_data is None:
                print(
                    f'Error occured while getting the final page of commits in the year {year}.')
                return None

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
        releases_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/releases?per_page=100'
        releases_data = self.try_perform_api_call(releases_url, constants.CORE)

        # Get the total download count
        total_download_count = 0
        while True:
            # Make sure we got a valid response
            if releases_data is None:
                print('Error occured while getting the total download count.')
                return None

            # Add the download count of all the application assets for every release on this page
            for release in releases_data.json():
                for asset in release['assets']:
                    if 'application' in asset['content_type']:
                        total_download_count += asset['download_count']

            # See if we still have pages to go
            # If so, make an API call to the next page
            if 'next' in releases_data.links:
                releases_url = releases_data.links['next']['url'] + \
                    '&per_page=100'
                releases_data = self.try_perform_api_call(
                    releases_url, constants.CORE)
            # Else stop the loop, as we are done
            else:
                break

        # Return the total download count
        return total_download_count

    def get_release_download_count(self, owner, repo, release):
        """
        Get the total amount of downloads of a specific release
        """
        print(f'Getting download count of release {release}...')

        # Get the information for the given release
        release_data = self.get_release_data(owner, repo, release)

        # Make sure we got a valid response
        if release_data is None:
            print(
                f'Error occured while getting the download count of release {release}.')
            return None

        # Get the download count per non-text released asset
        total_release_download_count = 0
        for asset in release_data['assets']:
            if 'application' in asset['content_type']:
                total_release_download_count += asset['download_count']

        # Return the total download count
        return total_release_download_count

    def get_zero_responses_issue_count(self, owner, repo):
        """
        Get the total amount of issues that have no responses
        """
        print('Getting zero-response issues count...')

        # Get the first page of issues
        issues_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/issues?per_page=100&state=open&sort=comments&direction=asc'
        issues_data = self.try_perform_api_call(issues_url, constants.CORE)
        last_full_no_responses_page = 0

        while True:
            # Make sure we got a valid response
            if issues_data is None:
                print('Error occured while getting the 0-response-issues count.')
                return None

            # See if there are more pages AND the last issue on this page has no responses
            # As if that is the case, we need to take a look a the next page
            if 'next' in issues_data.links and issues_data.json()[-1]['comments'] == 0:
                last_full_no_responses_page += 1
                issues_url = issues_data.links['next']['url'] + \
                    '&per_page=100&state=open&sort=comments&direction=asc'
                issues_data = self.try_perform_api_call(
                    issues_url, constants.CORE)
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
        issue_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/issues?per_page=100&state=closed&sort=created&direction=desc'
        issue_data = self.try_perform_api_call(issue_url, constants.CORE)

        # Make sure we got a valid response
        if issue_data is None:
            print('Error occured while getting the average issue resolution time.')
            return None

        # Add the issues of the first page to the JSON object
        all_issues = issue_data.json()

        # If there are more pages, add the next 100 issues to the JSON object as well
        # For now, we only use a maximum of 200 issues, as otherwise we would be making too many API calls
        if 'next' in issue_data.links:
            issue_url = issue_data.links['next']['url'] + \
                '&per_page=100&state=closed&sort=created&direction=desc'
            issue_data = self.try_perform_api_call(issue_url, constants.CORE)

            # Make sure we got a valid response
            if issue_data is None:
                print('Error occured while getting the average issue resolution time.')
                return None

            all_issues += issue_data.json()

        # Variable to store the total resolution time in seconds
        total_resolution_time = 0

        # Loop through all the issues, and add up the time between the issue creation and the issue resolution
        for issue in all_issues:
            # Calculate the resolution time
            creation_date = datetime.strptime(
                issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            closure_date = datetime.strptime(
                issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
            issue_resolution_time = closure_date - creation_date

            # Add the resolution time to the total
            total_resolution_time += issue_resolution_time.seconds

        # Return the average resolution time
        return total_resolution_time / len(all_issues)

    def issue_count_per_release(self, owner, repo, release):
        """
        Get the publish date of the given release
        and the release after it (if it exists)

        Then perform a search API call to find all issues that were posted between those dates
        """
        print(f'Getting issue count for release {release}...')

        # Get the publish dates of the given release and the release after it
        release_dates = self.get_release_dates(owner, repo, release)

        # Make sure we got a valid response
        if release_dates is None:
            print(
                f'Error occured while getting the issue count for release {release}.')
            return None

        # Extract the publish dates
        (given_release_date, next_release_date) = release_dates

        # Get the issues that were posted between the given release and the next release (if it exists)
        if next_release_date is None:
            issues_url = f'{constants.BASE_URL_SEARCH}/issues?q=is:issue+created:{given_release_date}..*+repo:{owner}/{repo}&per_page=100'
        else:
            issues_url = f'{constants.BASE_URL_SEARCH}/issues?q=is:issue+created:{given_release_date}..{next_release_date}+repo:{owner}/{repo}&per_page=100'

        # Get the first page of issues
        issues_data = self.try_perform_api_call(issues_url, constants.SEARCH)

        # Make sure we got a valid response
        if issues_data is None:
            print('Error occured while getting the issue count for release.')
            return None

        # Return this count
        return issues_data.json()['total_count']

    def get_release_dates(self, owner, repo, release):
        """
        Get the publish date of the given release and the release after it (if it exists)
        Presumes that the repository
        """

        # Get the information about the first releases
        releases_url = f'{constants.BASE_URL_REPOS}/{owner}/{repo}/releases?per_page=100'
        releases_data = self.try_perform_api_call(releases_url, constants.CORE)
        previous_page = None

        while True:
            # Make sure we got a valid response
            if releases_data is None:
                print('Error occured while getting the release dates.')
                return None

            # Get the json data for easy access
            releases_json = releases_data.json()

            # See if the current release is within the current page
            for i in range(len(releases_json)):
                # If it is, and there is an entry before the current one (aka later in time)
                # Return the publish dates of both
                if releases_json[i]['tag_name'] == release and i > 0:
                    return (releases_json[i]['published_at'], releases_json[i - 1]['published_at'])

                # If it is and there is no entry before the current one, but we have a previous page
                # Return the publish date of the current previous release on the previous page
                if releases_json[i]['tag_name'] == release and i == 0:
                    # If there is no previous page, return None for the previous release
                    if previous_page is None:
                        return (releases_json[i]['published_at'], None)

                    # Else return the publish date of the previous release
                    return (releases_json[i]['published_at'], previous_page.json()[-1]['published_at'])

            # If there is a next page, update previous_page and releases_data
            if 'next' in releases_data.links:
                # If the current release is not within the current page, check the next page
                previous_page = releases_data
                # Update releases_data by making a new API call to the given next page
                releases_url = releases_data.links['next']['url'] + \
                    '&per_page=100'
                releases_data = self.try_perform_api_call(
                    releases_url, constants.CORE)
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
        stargazer_url = f'{constants.BASE_URL_ORGS}/{owner}/repos?per_page=100'
        stargazer_data = self.try_perform_api_call(
            stargazer_url, constants.CORE)

        total_stargazer_count = 0

        while True:
            # Make sure we got a valid response
            if stargazer_data is None:
                print('Error occured while getting the stargazer count for owner.')
                return None

            # Loop through all the repositories of the owner
            for repo in stargazer_data.json():
                # Add the stargazer count of the current repository to the total
                total_stargazer_count += repo['stargazers_count']

            # If there is a next page, update stargazer_data
            if 'next' in stargazer_data.links:
                # Update stargazer_data by making a new API call to the given next page
                stargazer_url = stargazer_data.links['next']['url'] + \
                    '&per_page=100'
                stargazer_data = self.try_perform_api_call(
                    stargazer_url, constants.CORE)
            # Else, there are no more pages, so return the total stargazer count
            else:
                return total_stargazer_count

    def try_perform_api_call(self, api_url, call_type):
        """
        Perform rate limit checks, and if those pass, perform an API call

        If successful, returns the response
        If not, returns None
        """

        # Check if we still have API calls left
        if self.check_rate_limit(call_type):
            # Decrement the rate limit of the given type
            if call_type == constants.CORE:
                self.core_remaining -= 1
            elif call_type == constants.SEARCH:
                self.search_remaining -= 1

            # Return the response, no matter if it succeeded or not
            return make_api_call(api_url, constants.API_GITHUB)

        # If we don't have any API calls left, return None
        return None

    def check_rate_limit(self, call_type):
        """
        Function to check if a rate limit has been reached

        Returns true if we can continue with the API call
        Else it will return false
        """

        # Check locally if we still have API calls left
        # If not, check if the rate limits have changed
        if (call_type == constants.CORE and self.core_remaining == 0) or (call_type == constants.SEARCH and self.search_remaining == 0):
            # Try to update the rate limit data
            if self.update_rate_limit_data():
                # If the update was successful, check the rate limits again
                if call_type == constants.CORE and self.core_remaining == 0:
                    print('Core rate limit reached.')
                    return False
                elif call_type == constants.SEARCH and self.search_remaining == 0:
                    print('Search rate limit reached.')
                    return False
            else:
                # If the update was unsuccessful, return false
                return False
        # If our local count is still above 0, return true
        return True

    def update_rate_limit_data(self):
        """
        Makes an API call in order to get (and update) the rate limit data

        Returns true if the data was updated successfully
        Else it will return false
        """

        # Make the API call
        rate_limit_response = make_api_call(
            constants.BASE_URL_RATE, constants.API_GITHUB)

        # See if the response we got is valid
        if rate_limit_response is not None:
            rate_limit_data = rate_limit_response.json()

            self.core_remaining = int(
                rate_limit_data['resources']['core']['remaining'])
            self.search_remaining = int(
                rate_limit_data['resources']['search']['remaining'])

            # Tell the user how many API calls they have left
            print(f'Core rate-limit remaining: {self.core_remaining}')
            print(f'Search rate-limit remaining: {self.search_remaining}')

            return True
        else:
            return False
