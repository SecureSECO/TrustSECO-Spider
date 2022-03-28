"""
File containing the unit tests for the github_spider.py file.
"""

# Unit testing imports
import responses
# Spider import
import github_spider_bs as spider


class TestUserCount:
    """
    Test the get_repository_user_count function.

    We will test the following scenario's:
    1. The get request failed
        - The response code is not 200
        - The response body is empty
    2. The get request succeeded but the number of users is not found
        - The response body is empty
        - The 'used by' <a> tag is not found
        - The 'used by' <a> tag has no 'title' attribute
    3. The get request succeeded and the number of users is found

    """

    owner = 'numpy'
    repo = 'numpy'
    url = f'https://github.com/{owner}/{repo}'
    empty_body = ''

    def get_regular_body(self):
        with open('GitHub/test_files/user_count/regular.txt', 'r') as regular:
            regular_body = regular.read()
        return regular_body

    def get_no_tag_body(self):
        with open('GitHub/test_files/user_count/no_a_tag.txt', 'r') as no_tag:
            no_tag_body = no_tag.read()
        return no_tag_body

    def get_no_title_body(self):
        with open('GitHub/test_files/user_count/no_title_attribute.txt', 'r') as no_title:
            no_title_body = no_title.read()
        return no_title_body

    @responses.activate
    def test_invalid_response_code(self):
        regular_body = self.get_regular_body()
        responses.add(
            responses.GET, self.url, body=regular_body, status=404)
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the get request failed
        assert result is None

    @responses.activate
    def test_empty_response_body(self):
        responses.add(
            responses.GET, self.url, body=self.empty_body, status=200)
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the response had no body, hence no user count could be found
        assert result is None

    @responses.activate
    def test_no_tag_found(self):
        no_tag_body = self.get_no_tag_body()
        responses.add(
            responses.GET, self.url, body=no_tag_body, status=200)
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the 'used by' <a> tag was not found
        assert result is None

    @responses.activate
    def test_no_title_attribute(self):
        no_title_body = self.get_no_title_body()
        responses.add(
            responses.GET, self.url, body=no_title_body, status=200)
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the 'used by' <a> tag had no 'title' attribute
        assert result is None

    @responses.activate
    def test_user_count_found(self):
        regular_body = self.get_regular_body()
        responses.add(
            responses.GET, self.url, body=regular_body, status=200)
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be the number of users
        assert result == 975170


class TestIssueRatio:
    """
    Test the get_repository_issue_ratio function.

    We will test the following scenario's:
    1. The get request failed
        - The response code is not 200
        - The response body is empty
    2. The get request succeeded but the issue ratio is not found
        - The response body is empty
        - The open issue count is not found
        - The open issue count is 0
        - The closed issue count is not found
        - The closed issue count is 0
    3. The get request succeeded and the issue ratio is found

    """

    owner = 'numpy'
    repo = 'numpy'
    url = f'https://github.com/{owner}/{repo}/issues'
    empty_body = ''

    def get_regular_body(self):
        with open('GitHub/test_files/issue_ratio/regular.txt', 'r', encoding='iso-8859-15') as regular:
            regular_body = regular.read()
        return regular_body

    def get_no_open_body(self):
        with open('GitHub/test_files/issue_ratio/no_open_issues.txt', 'r', encoding='iso-8859-15') as no_open:
            no_open_body = no_open.read()
        return no_open_body

    def get_zero_open_body(self):
        with open('GitHub/test_files/issue_ratio/zero_open_issues.txt', 'r', encoding='iso-8859-15') as zero_open:
            zero_open_body = zero_open.read()
        return zero_open_body

    def get_no_closed_body(self):
        with open('GitHub/test_files/issue_ratio/no_closed_issues.txt', 'r', encoding='iso-8859-15') as no_closed:
            no_closed_body = no_closed.read()
        return no_closed_body

    def get_zero_closed_body(self):
        with open('GitHub/test_files/issue_ratio/zero_closed_issues.txt', 'r', encoding='iso-8859-15') as zero_closed:
            zero_closed_body = zero_closed.read()
        return zero_closed_body

    @ responses.activate
    def test_invalid_response_code(self):
        regular_body = self.get_regular_body()
        responses.add(
            responses.GET, self.url, body=regular_body, status=404)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be None as the get request failed
        assert result is None

    @ responses.activate
    def test_empty_response_body(self):
        responses.add(
            responses.GET, self.url, body=self.empty_body, status=200)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be None as the response had no body, hence no issue ratio could be found
        assert result is None

    @ responses.activate
    def test_no_open_issues(self):
        no_open_body = self.get_no_open_body()
        responses.add(
            responses.GET, self.url, body=no_open_body, status=200)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be None as the open issue count was not found
        assert result is None

    @ responses.activate
    def test_zero_open_issues(self):
        zero_open_body = self.get_zero_open_body()
        responses.add(
            responses.GET, self.url, body=zero_open_body, status=200)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be None as the open issue count was 0
        assert result == 0.0

    @ responses.activate
    def test_no_closed_issues(self):
        no_closed_body = self.get_no_closed_body()
        responses.add(
            responses.GET, self.url, body=no_closed_body, status=200)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be None as the closed issue count was not found
        assert result is None

    @ responses.activate
    def test_zero_closed_issues(self):
        zero_closed_body = self.get_zero_closed_body()
        responses.add(
            responses.GET, self.url, body=zero_closed_body, status=200)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be None as the closed issue count was 0
        assert result is None

    @ responses.activate
    def test_issue_ratio_found(self):
        regular_body = self.get_regular_body()
        responses.add(
            responses.GET, self.url, body=regular_body, status=200)
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be the issue ratio
        assert result == 0.24156432574222012
