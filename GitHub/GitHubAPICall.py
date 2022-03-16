import requests
import json

"""doctsting"""
class GitHubAPICall:
    # Base URLs
    def __init__(self):
        self.base_url_repos  = "https://api.github.com/repos/"
        self.base_url_users  = "https://api.github.com/users/"
        self.base_url_search = "https://api.github.com/search/repositories?q="

    # Get the information of the owner, of the repository, and of the specific version.
    def get_all_data(self, owner, repo, version, year, user_token):
        # Get the individual data-points
        repository_data = self.get_basic_repository_data(owner, repo, user_token)
        version_data = self.get_version_data(owner, repo, version, user_token)
        owner_data = self.get_owner_data(owner, user_token)
        contributor_count = self.get_repository_contributor_count(owner, repo, user_token)
        gitstar_ranking = self.get_gitstar_ranking(owner, repo, repository_data['language'], user_token, repository_data['stargazers_count'])
        yearly_commit_count = self.get_yearly_commit_count(owner, repo, user_token)
        
        # Return a JSON object containing all the data
        return {
            'repository_data': repository_data,
            'version_data': version_data,
            'owner_data': owner_data,
            'contributor_count': contributor_count,
            'gitstar_ranking': gitstar_ranking,
            'yearly_commit_count': yearly_commit_count
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
        api_url = self.base_url_search + 'stars:>0+language:' + language + '&sort=stars&order=desc&per_page=100'
        data = self.make_api_call(api_url, user_token)

        # See if the result has multiple pages
        # If it does, perform a binary search to find the page with the given repository
        if 'last' in data.links:
            # Get the total amount of pages
            page_count = data.links['last']['url'].split('=')[-1]

            # Make sure that our repository's stargazer count is above the lowest query-able stargazer count
            final_page_data = self.make_api_call(data.links['last']['url'], user_token)
            final_repo_star_count = final_page_data.json()['items'][-1]['stargazers_count']
            # If the our count is lower, return none
            if final_repo_star_count > star_count:
                return None

            # Perform binary searching to find the correct page
            lower_bound = 0
            upper_bound = int(page_count)
            base_url = api_url + '&page='
            while True:
                # Calculate the index of the middle page, and get the data from that page
                middle_page_number = int((upper_bound + lower_bound) / 2)
                api_url = base_url + str(middle_page_number)
                page_data = self.make_api_call(api_url, user_token).json()

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
            for repo in data.json()['items']:
                if repo['full_name'] == owner + '/' + repo:
                    return repo['stargazers_count']
            
            # If we didn't find the repository, return None
            return None

    # Get the amount of commits in the given year
    def get_specific_yearly_commit_count(self, owner, repo, year, user_token):
        # Get the commits for the given year
        commits_url = self.base_url_repos + owner + '/' + repo + '/commits?per_page=100&since=' + str(year) + '-01-01T00:00:00Z&until=' + str(year) + '-12-31T23:59:59Z'
        commits_data = self.make_api_call(commits_url, user_token)

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

        # Get the download count per non-text released asset
        total_version_download_count = 0
        for asset in version_data.json()['assets']:
            if 'application' in asset['content_type']:
                total_version_download_count += asset['download_count']
        
        # Return the total download count
        return total_version_download_count

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

        
#example test function for github actions
def addOne(arg):
  return arg+1
