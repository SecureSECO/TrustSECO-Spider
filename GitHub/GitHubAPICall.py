import requests
from datetime import datetime

class GitHubAPICall:
    # Base URLs
    def __init__(self):
        self.base_url_repos  = "https://api.github.com/repos/"
        self.base_url_users  = "https://api.github.com/users/"
        self.base_url_search = "https://api.github.com/search/repositories?q="

    # Get the information of the owner, of the repository, and of the specific version.
    def get_all_data(self, owner, repo, version, year, user_token):
        # Get the individual data-points
        print('Getting repository data...')
        repository_data = self.get_basic_repository_data(owner, repo, user_token)
        print('Getting version data...')
        version_data = self.get_version_data(owner, repo, version, user_token)
        print('Getting owner data...')
        owner_data = self.get_owner_data(owner, user_token)
        print('Getting contributor count...')
        contributor_count = self.get_repository_contributor_count(owner, repo, user_token)
        print('Getting GitStar ranking...')
        gitstar_ranking = self.get_gitstar_ranking(owner, repo, repository_data['language'], user_token, repository_data['stargazers_count'])
        print('Getting yearly commit count...')
        yearly_commit_count = self.get_yearly_commit_count(owner, repo, user_token)
        print('Getting commit count in year ' + str(year) + '...')
        commit_count_in_year = self.get_commit_count_in_year(owner, repo, year, user_token)
        print('Getting total download count...')
        total_download_count = self.get_total_download_count(owner, repo, user_token)
        print('Getting download count of version ' + version + '...')
        version_download_count = self.get_version_download_count(owner, repo, version, user_token)
        print('Getting zero-response issues count...')
        zero_response_issues_count = self.get_zero_responses_issue_count(owner, repo, user_token)
        print('Getting average issue resolution time...')
        average_issue_resolution_time = self.get_average_issue_resolution_time(owner, repo, user_token)
        
        # Return a JSON object containing all the data
        return {
            'repository_data': repository_data,
            'version_data': version_data,
            'owner_data': owner_data,
            'contributor_count': contributor_count,
            'gitstar_ranking': gitstar_ranking,
            'yearly_commit_count': yearly_commit_count,
            'commit_count_in_year': commit_count_in_year,
            'total_download_count': total_download_count,
            'version_download_count': version_download_count,
            'zero_response_issues_count': zero_response_issues_count,
            'average_issue_resolution_time': average_issue_resolution_time
        }

    # Get the basic information about the given repository
    # Contains the language, #open_issues, 
    def get_basic_repository_data(self, owner, repo, user_token):
        # Get the basic repository data
        repository_data = self.make_api_call(self.base_url_repos + owner + '/' + repo, user_token)

        # Return the data
        return repository_data.json()

    # Get information about a specific version/release of a repository
    def get_version_data(self, owner, repo, version, user_token):
        # Get the basic repository data
        version_data = self.make_api_call(self.base_url_repos + owner + '/' + repo + '/releases/tags/' + version, user_token)

        # Return the data
        return version_data.json()

    # Get the basic information about the repository owner
    def get_owner_data(self, owner, user_token):
        # Get the user data
        owner_data = self.make_api_call(self.base_url_users + owner, user_token)

        # Return the data
        return owner_data.json()

    # Get the amount of contributors of the given repository
    def get_repository_contributor_count(self, owner, repo, user_token):
        # Get the contributors of the repository
        contributors_url = self.base_url_repos + owner + '/' + repo + '/contributors?per_page=100&anon=1'
        contributors_data = self.make_api_call(contributors_url, user_token)
        
        # Very simple error handling
        if contributors_data is None:
            print('Error occured while getting the contributor count.')
            return None

        # See if this repository has multiple pages of contributors
        if 'last' in contributors_data.links:
            # Get the amount of contributors on the final page
            final_page_data = self.make_api_call(contributors_data.links['last']['url'], user_token)
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

    # Get the GitStar ranking of the given repository
    # If the repository is not ranked, return None
    # Else, return the ranking
    def get_gitstar_ranking(self, owner, repo, language, user_token, star_count):
        # Perform a basic search to list all the repositories in the given language, sorted by their stargazer count
        ranking_url = self.base_url_search + 'stars:>0+language:' + language + '&sort=stars&order=desc&per_page=100'
        ranking_data = self.make_api_call(ranking_url, user_token)
        
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
            final_page_data = self.make_api_call(ranking_data.links['last']['url'], user_token)
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
                page_data = self.make_api_call(ranking_url, user_token).json()

                # Get the highest and lowest stargazer counts from the query
                page_highest_star_count = page_data['items'][0]['stargazers_count']
                page_lowest_star_count = page_data['items'][-1]['stargazers_count']

                # See if the stargazer count of the wanted repository is within the bounds of the current page
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
            for repo in ranking_data.json()['items']:
                if repo['full_name'] == owner + '/' + repo:
                    return repo['stargazers_count']
            
            # If we didn't find the repository, return None
            return None

    # Get the amount of commits in the given year
    def get_commit_count_in_year(self, owner, repo, year, user_token):
        # Get the commits for the given year
        commits_url = self.base_url_repos + owner + '/' + repo + '/commits?per_page=100&since=' + str(year) + '-01-01T00:00:00Z&until=' + str(year) + '-12-31T23:59:59Z'
        commits_data = self.make_api_call(commits_url, user_token)
        
        # Very simple error handling
        if commits_data is None:
            print('Error occured while getting the commit count in the year ' + str(year), '.')
            return None

        # See if there are multiple pages of commits
        if 'last' in commits_data.links:
            # Get the amount of commits on the final page
            final_page_data = self.make_api_call(commits_data.links['last']['url'], user_token)
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
    
    # Get the amount of commits in the last year
    def get_yearly_commit_count(self, owner, repo, user_token):
        # Get all the commits for the past year
        commits_url = self.base_url_repos + owner + '/' + repo + '/stats/commit_activity'
        commits_data = self.make_api_call(commits_url, user_token)
        
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

    # Get the total amount of downloads of this package
    def get_total_download_count(self, owner, repo, user_token):
        # Get the first page of releases
        releases_url = self.base_url_repos + owner + '/' + repo + '/releases?per_page=100'
        releases_data = self.make_api_call(releases_url, user_token)
        
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
                releases_data = self.make_api_call(releases_url, user_token)
            # Else stop the loop, as we are done
            else:
                break

        # Return the total download count
        return total_download_count

    # Get the total amount of downloads of a specific version
    def get_version_download_count(self, owner, repo, version, user_token):
        # Get the information for the given release
        version_url = self.base_url_repos + owner + '/' + repo + '/releases/tags/' + version
        version_data = self.make_api_call(version_url, user_token)
        
        # Very simple error handling
        if version_data is None:
            print('Error occured while getting the download count of release ' + version + '.')
            return None

        # Get the download count per non-text released asset
        total_version_download_count = 0
        for asset in version_data.json()['assets']:
            if 'application' in asset['content_type']:
                total_version_download_count += asset['download_count']
        
        # Return the total download count
        return total_version_download_count

    # Get the total amount of issues that have no responses
    def get_zero_responses_issue_count(self, owner, repo, user_token):
        issues_url = self.base_url_repos + owner + '/' + repo + '/issues?per_page=100&state=open&sort=comments&direction=asc'
        issues_data = self.make_api_call(issues_url, user_token)
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
                issues_data = self.make_api_call(issues_url, user_token)
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

    # Get the average resolution time of the last 200 issues
    # Returns the average resolution time in seconds
    def get_average_issue_resolution_time(self, owner, repo, user_token):
        # Get the first page of closed issues
        issue_url = self.base_url_repos + owner + '/' + repo + '/issues?per_page=100&state=closed&sort=created&direction=desc'
        issue_data = self.make_api_call(issue_url, user_token)
        
        # Very simple error handling
        if issue_data is None:
            print('Error occured while getting the average issue resolution time.')
            return None

        # Add the issues of the first page to the JSON object
        all_issues = issue_data.json()

        # If there are more pages, add the next 100 issues to the JSON object as well
        # For now, we only use a maximum of 200 issues, as otherwise we would be making too many API calls
        if 'next' in issue_data.links:
            issue_url = issue_data.links['next']['url'] + '&per_page=100&state=closed&sort=created&direction=desc'
            issue_data = self.make_api_call(issue_url, user_token)
            all_issues += issue_data.json()

        # Variable to store the total resolution time in seconds
        total_resolution_time = 0

        # Loop through all the issues, and add up the time between the issue creation and the issue resolution
        for issue in all_issues:
            # Calculate the resolution time
            creation_date = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            closure_date = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
            issue_resolution_time = closure_date - creation_date
            
            # Add the resolution time to the total
            total_resolution_time += issue_resolution_time.seconds

        # Return the average resolution time
        return total_resolution_time / len(all_issues)

    # Perform a simple GET request, based off the given URL
    def make_api_call(self, api_url, user_token, given_headers = None):
        # Define the header
        headers = {'Authorization': 'token ' + user_token,
                   'Accept': 'application/vnd.github.v3+json'}

        # Add the given headers, if any
        if not given_headers is None:
            headers.update(given_headers)

        # Basic request to get the information.
        data_response = requests.get(api_url,headers=headers)

        # See if we got a valid response
        if data_response.status_code == 200:
            data = data_response
        else:
            print('Unable to get data from GitHub')
            print('Error: ' + data_response.text)
            data = None
            
        return data