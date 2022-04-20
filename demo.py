"""
Basic demo file, purely for demonstration purposes.

Allows the user to test the Device Flow authentication process,
GitHub API calls, and spidering.
"""
# For getting additional arguments from the command line
import sys
# For json converting
import json
# For accessing the GitHub data-points
import interface


def gh_complete_demo(owner, repo, year=None, version=None, include_search=False):
    """
    Demo showing all of the currently available data-points from GitHub
    """

    data = {
        'contributor_count': interface.gh_get_contributor_count(owner, repo),
        'repository_user_count': interface.gh_get_repository_user_count(owner, repo),
        'total_download_count': interface.gh_get_total_download_count(owner, repo),
        'yearly_commit_count': interface.gh_get_yearly_commit_count(owner, repo),
        'repository_language': interface.gh_get_repository_language(owner, repo),
        'open_issue_count': interface.gh_get_open_issue_count(owner, repo),
        'zero_responses_issue_count': interface.gh_get_zero_responses_issue_count(owner, repo),
        'issue_ratio': interface.gh_get_repository_issue_ratio(owner, repo),
        'average_issue_resolution_time': interface.gh_get_average_issue_resolution_time(owner, repo),
        'owner_stargazer_count': interface.gh_get_owner_stargazer_count(owner)
    }

    if year is not None:
        data['commit_count_in_year'] = interface.gh_get_commit_count_in_year(
            owner, repo, year)

    if version is not None:
        data[
            'release_download_count'] = interface.gh_get_release_download_count(owner, repo, version)

    if include_search:
        data['gitstar_ranking'] = interface.gh_get_gitstar_ranking(owner, repo)

        if year is not None:
            data['release_issue_count'] = interface.gh_get_release_issue_count(
                owner, repo, version)

    print('---------------------------------------------------')
    print(f'GitHub data for {owner}/{repo}')
    print(json.dumps(data, indent=4))
    print('---------------------------------------------------')


def lib_complete_demo(platform, owner, name, version):
    """
    Demo showing all of the currently available data-points from Libraries.io
    """

    data = {
        'release_frequency': interface.lib_get_release_frequency(platform, name),
        'contributor_count': interface.lib_get_contributor_count(owner, name),
        'dependency_count': interface.lib_get_dependency_count(platform, name, version),
        'dependent_count': interface.lib_get_dependent_count(platform, name),
        'latest_release': interface.lib_get_latest_release_date(platform, name),
        'first_release': interface.lib_get_first_release_date(platform, name),
        'release_count': interface.lib_get_release_count(platform, name),
        'sourcerank': interface.lib_get_sourcerank(platform, name)
    }

    print('---------------------------------------------------')
    print(f'Libraries.io data for {name} on {platform}')
    print(json.dumps(data, indent=4))
    print('---------------------------------------------------')


def start_demo(include_search=False):
    # Numpy
    gh_complete_demo(owner='numpy', repo='numpy', year=2021,
                     version='v1.22.1', include_search=include_search)

    lib_complete_demo(platform='Pypi', owner='numpy',
                      name='numpy', version='1.22.1')


if __name__ == '__main__':
    # See if the user passed arguments
    if len(sys.argv) > 1:
        # See if the passed argument contains 'search', as we have to include SEARCH API calls
        if 'gh_search' in sys.argv[1]:
            print('Running the demo, including search API calls.')
            start_demo(include_search=True)
        else:
            print(
                'Did not recognise the argument, running the demo without search API calls.')
            start_demo()
    else:
        print('No arguments passed, running demo without search.')
        print('To run with search, pass "search" as an argument.')
        start_demo()
