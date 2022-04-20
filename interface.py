"""
Interface file that summarizes the functions that are available,
in terms of what the API calls and spidering can do.
"""

# Import all the classes that gather data
from GitHub.github_api_calls import GitHubAPICall
from GitHub.github_spider_bs import GitHubSpider
from LibrariesIO.libaries_io_api_calls import LibrariesAPICall

# Data requesting objects
gh_calls = GitHubAPICall()
gh_spider = GitHubSpider()
lib_calls = LibrariesAPICall()


def testfunc(imput):
    return imput * 2


# region GitHub
def gh_get_contributor_count(owner, repo):
    """
    Gets the number of contributors for a given repository
    """
    return gh_calls.get_repository_contributor_count(owner, repo)


def gh_get_repository_user_count(owner, repo):
    """
    Gets amount of users of a given repository
    """
    return gh_spider.get_repository_user_count(owner, repo)


def gh_get_total_download_count(owner, repo):
    """
    Gets the total download count for a given repository
    """
    return gh_calls.get_total_download_count(owner, repo)


def gh_get_release_download_count(owner, repo, release):
    """
    Gets the download count for a given release
    """
    return gh_calls.get_release_download_count(owner, repo, release)


def gh_get_yearly_commit_count(owner, repo):
    """
    Gets the commit count for the last year
    """
    return gh_calls.get_yearly_commit_count(owner, repo)


def gh_get_commit_count_in_year(owner, repo, year):
    """
    Gets the commit count for a given year
    """
    return gh_calls.get_commit_count_in_year(owner, repo, year)


def gh_get_repository_language(owner, repo):
    """
    Gets the language of the repository
    """
    return gh_calls.get_repository_language(owner, repo)


def gh_get_gitstar_ranking(owner, repo):
    """
    Gets the gitstar score of the repository
    """
    return gh_calls.get_gitstar_ranking(owner, repo)


def gh_get_open_issue_count(owner, repo):
    """
    Gets the open issue count of the repository
    """
    return gh_spider.get_repository_open_issue_count(owner, repo)


def gh_get_zero_responses_issue_count(owner, repo):
    """
    Gets the zero response issue count of the repository
    """
    return gh_calls.get_zero_responses_issue_count(owner, repo)


def gh_get_release_issue_count(owner, repo, release):
    """
    Gets the issue count for a given release
    """
    return gh_calls.issue_count_per_release(owner, repo, release)


def gh_get_repository_issue_ratio(owner, repo):
    """
    Gets the issue ratio of a given repository
    """
    return gh_spider.get_repository_issue_ratio(owner, repo)


def gh_get_average_issue_resolution_time(owner, repo):
    """
    Gets the average issue resolution time
    """
    return gh_calls.get_average_issue_resolution_time(owner, repo)


def gh_get_owner_stargazer_count(owner):
    """
    Gets the stargazer count of the owner
    """
    return gh_calls.get_owner_stargazer_count(owner)
# endregion


# region LibrariesIO
def lib_get_release_frequency(platform, name):
    """
    Gets the average release frequency of the given package
    """
    return lib_calls.get_release_frequency(platform, name)


def lib_get_contributor_count(owner, name):
    """
    Gets the contributor count of the given package
    """
    return lib_calls.get_contributors_count(owner, name)


def lib_get_dependency_count(platform, name, version):
    """
    Gets the dependency count of the given package
    """
    return lib_calls.get_dependency_count(platform, name, version)


def lib_get_dependent_count(platform, name):
    """
    Gets the dependent count of the given package
    """
    return lib_calls.get_dependent_count(platform, name)


def lib_get_latest_release_date(platform, name):
    """
    Gets the latest release date of the given package
    """
    return lib_calls.get_latest_release_date(platform, name)


def lib_get_first_release_date(platform, name):
    """
    Gets the first release date of the given package
    """
    return lib_calls.get_first_release_date(platform, name)


def lib_get_release_count(platform, name):
    """
    Gets the release count of the given package
    """
    return lib_calls.get_release_count(platform, name)


def lib_get_sourcerank(platform, name):
    """
    Gets the sourcerank of the given package
    """
    return lib_calls.get_sourcerank(platform, name)
# endregion
