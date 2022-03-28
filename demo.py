"""
Basic demo file, purely for demonstration purposes.

Allows the user to test the Device Flow authentication process,
GitHub API calls, and spidering.
"""

# For json converting
import json
# For accessing the GitHub data-points
import interface


def complete_demo(owner, repo, year=None, version=None, include_search=False):
    """
    Demo showing all of the currently available data-points
    """

    data = {
        'contributor_count': interface.get_contributor_count(owner, repo),
        'repository_user_count': interface.get_repository_user_count(owner, repo),
        'total_download_count': interface.get_total_download_count(owner, repo),
        'yearly_commit_count': interface.get_yearly_commit_count(owner, repo),
        'repository_language': interface.get_repository_language(owner, repo),
        'open_issue_count': interface.get_open_issue_count(owner, repo),
        'zero_responses_issue_count': interface.get_zero_responses_issue_count(owner, repo),
        'issue_ratio': interface.get_repository_issue_ratio(owner, repo),
        'average_issue_resolution_time': interface.get_average_issue_resolution_time(owner, repo),
        'owner_stargazer_count': interface.get_owner_stargazer_count(owner)
    }

    if year is not None:
        data['commit_count_in_year'] = interface.get_commit_count_in_year(
            owner, repo, year)

    if version is not None:
        data[
            'release_download_count'] = interface.get_release_download_count(owner, repo, version)

    if include_search:
        data['gitstar_ranking'] = interface.get_gitstar_ranking(owner, repo)

        if year is not None:
            data['release_issue_count'] = interface.get_release_issue_count(
                owner, repo, version)

    print('---------------------------------------------------')
    print(f'Data for {owner}/{repo}')
    print(json.dumps(data, indent=4))
    print('---------------------------------------------------')


# Numpy
complete_demo(owner='numpy', repo='numpy', year=2021, version='v1.22.1')

# Random repo
complete_demo('TheAlgorithms', 'Python')
