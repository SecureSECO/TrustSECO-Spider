"""
Interface file that summarizes the functions that are available,
in terms of what the API calls and spidering can do.
"""

# API calls
import GitHub.github_api_calls as github_api_calls
import GitHub.github_spider_bs as github_spider

# API call object
api_calls = github_api_calls.GitHubAPICall()


def get_contributor_count(owner, repo):
    """
    Gets the number of contributors for a given repository
    """
    return api_calls.get_repository_contributor_count(owner, repo)


def get_repository_user_count(owner, repo):
    """
    Gets amount of users of a given repository
    """
    return github_spider.get_repository_user_count(owner, repo)


def get_total_download_count(owner, repo):
    """
    Gets the total download count for a given repository
    """
    return api_calls.get_total_download_count(owner, repo)


def get_release_download_count(owner, repo, release):
    """
    Gets the download count for a given release
    """
    return api_calls.get_release_download_count(owner, repo, release)


def get_yearly_commit_count(owner, repo):
    """
    Gets the commit count for the last year
    """
    return api_calls.get_yearly_commit_count(owner, repo)


def get_commit_count_in_year(owner, repo, year):
    """
    Gets the commit count for a given year
    """
    return api_calls.get_commit_count_in_year(owner, repo, year)


def get_repository_language(owner, repo):
    """
    Gets the language of the repository
    """
    return api_calls.get_repository_language(owner, repo)


def get_gitstar_ranking(owner, repo):
    """
    Gets the gitstar score of the repository
    """
    return api_calls.get_gitstar_ranking(owner, repo)


def get_open_issue_count(owner, repo):
    """
    Gets the open issue count of the repository
    """
    return github_spider.get_repository_open_issue_count(owner, repo)


def get_zero_responses_issue_count(owner, repo):
    """
    Gets the zero response issue count of the repository
    """
    return api_calls.get_zero_responses_issue_count(owner, repo)


def get_release_issue_count(owner, repo, release):
    """
    Gets the issue count for a given release
    """
    return api_calls.issue_count_per_release(owner, repo, release)


def get_repository_issue_ratio(owner, repo):
    """
    Gets the issue ratio of a given repository
    """
    return github_spider.get_repository_issue_ratio(owner, repo)


def get_average_issue_resolution_time(owner, repo):
    """
    Gets the average issue resolution time
    """
    return api_calls.get_average_issue_resolution_time(owner, repo)


def get_owner_stargazer_count(owner):
    """
    Gets the stargazer count of the owner
    """
    return api_calls.get_owner_stargazer_count(owner)
