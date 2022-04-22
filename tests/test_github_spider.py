"""
File containing the unit tests for the github_spider.py file.
"""

# Unit testing imports
from unittest import mock
import responses
# Spider import
from GitHub.github_spider import GitHubSpider
spider = GitHubSpider()


class FileIOForTests:
    """
    Functions to get the needed text files for the tests.

    We are using the encoding parameter as to avoid errors when parsing the text files
    """

    # Test users
    def get_regular_body_users():
        with open('tests/test_files/user_count/regular.txt', 'r', encoding='iso-8859-15') as regular:
            regular_body = regular.read()
        return regular_body

    def get_no_tag_body_users():
        with open('tests/test_files/user_count/no_a_tag.txt', 'r', encoding='iso-8859-15') as no_tag:
            no_tag_body = no_tag.read()
        return no_tag_body

    def get_no_title_body_users():
        with open('tests/test_files/user_count/no_title_attribute.txt', 'r', encoding='iso-8859-15') as no_title:
            no_title_body = no_title.read()
        return no_title_body

    # Test issues
    def get_regular_body_issues():
        with open('tests/test_files/issue_ratio/regular.txt', 'r', encoding='iso-8859-15') as regular:
            regular_body = regular.read()
        return regular_body

    def get_no_open_body_issues():
        with open('tests/test_files/issue_ratio/no_open_issues.txt', 'r', encoding='iso-8859-15') as no_open:
            no_open_body = no_open.read()
        return no_open_body

    def get_zero_open_body_issues():
        with open('tests/test_files/issue_ratio/zero_open_issues.txt', 'r', encoding='iso-8859-15') as zero_open:
            zero_open_body = zero_open.read()
        return zero_open_body

    def get_no_closed_body_issues():
        with open('tests/test_files/issue_ratio/no_closed_issues.txt', 'r', encoding='iso-8859-15') as no_closed:
            no_closed_body = no_closed.read()
        return no_closed_body

    def get_zero_closed_body_issues():
        with open('tests/test_files/issue_ratio/zero_closed_issues.txt', 'r', encoding='iso-8859-15') as zero_closed:
            zero_closed_body = zero_closed.read()
        return zero_closed_body


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

    @ responses.activate
    def test_invalid_response_code(self):
        """
        Test for when the request returns an invalid response, i.e. a response with a code other than 200

        Return value should be None, as the request failed
        """
        # Get the mock response body
        regular_body = FileIOForTests.get_regular_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=404)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the get request failed
        assert result is None

    @ responses.activate
    def test_empty_response_body(self):
        """
        Test for when the request body is empty

        Return value should be None, as there is no way to find the open issue count
        """
        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body='', status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the response had no body, hence no user count could be found
        assert result is None

    @ responses.activate
    def test_user_count_tag_not_found(self):
        """
        Test for when the request body is not empty but the 'used by' <a> tag can not be found

        Return value should be None, as there is no way to find the user count
        """
        # Get the mock response body
        no_tag_body = FileIOForTests.get_no_tag_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=no_tag_body, status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the 'used by' <a> tag was not found
        assert result is None

    @ responses.activate
    def test_no_title_attribute(self):
        """
        Test for when the request body is not empty, and the 'used by' <a> tag is found, but the tag does not have a 'title' attribute

        Return value should be None, as there is no way to find the user count
        """
        # Get the mock response body
        no_title_body = FileIOForTests.get_no_title_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=no_title_body, status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the 'used by' <a> tag had no 'title' attribute
        assert result is None

    @ responses.activate
    def test_user_count_found(self):
        """
        Test for when the request body is not empty, and the 'used by' <a> tag is found, and the tag has a 'title' attribute

        Return value should be the number of users
        """
        # Get the mock response body
        regular_body = FileIOForTests.get_regular_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be the number of users
        assert result == 975170


class TestOpenIssues:
    """
    Test the get_repository_open_issue_count function.

    We will test the following scenario's:
    1. The get request failed
        - The response code is not 200
        - The response body is empty
    2. The get request succeeded but the open issue count is not found
    3. The get request succeeded and the open issue count is found
    """

    owner = 'numpy'
    repo = 'numpy'
    url = f'https://github.com/{owner}/{repo}/issues'

    @ responses.activate
    def test_invalid_response_code(self):
        """
        Test for when the request returns an invalid response, i.e. a response with a code other than 200

        Return value should be None, as the request failed
        """
        # Get the mock response body
        regular_body = FileIOForTests.get_regular_body_issues()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=404)

        # Get the result
        result = spider.get_repository_open_issue_count(self.owner, self.repo)

        # The result should be None as the get request failed
        assert result is None

    @ responses.activate
    def test_empty_response_body(self):
        """
        Test for when the request body is empty

        Return value should be None, as there is no way to find the open issue count
        """
        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body='', status=200)

        # Get the result
        result = spider.get_repository_open_issue_count(self.owner, self.repo)

        # The result should be None as the response had no body, hence no issue count could be found
        assert result is None

    @ responses.activate
    def test_no_open_issues(self):
        """
        Test for when the request body is not empty, but the open issue count can not be found

        Return value should be None, as there is no way to find the open issue count
        """
        # Get the mock response body
        no_open_body = FileIOForTests.get_no_open_body_issues()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=no_open_body, status=200)

        # Get the result
        result = spider.get_repository_open_issue_count(self.owner, self.repo)

        # The result should be None as the open issue count was not found
        assert result is None

    @responses.activate
    def test_open_issue_count_found(self):
        """
        Test for when the request body is not empty, and the open issue count is found

        Return value should be the open issue count
        """
        # Get the mock response body
        regular_body = FileIOForTests.get_regular_body_issues()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=200)

        # Get the result
        result = spider.get_repository_open_issue_count(self.owner, self.repo)

        # The result should be the open issue count
        assert result == 2026


class TestClosedIssues:
    """
    Test the get_repository_closed_issue_count function.

    We will test the following scenario's:
    1. The get request failed
        - The response code is not 200
        - The response body is empty
    2. The get request succeeded but the closed issue count is not found
    3. The get request succeeded and the closed issue count is found
    """

    owner = 'numpy'
    repo = 'numpy'
    url = f'https://github.com/{owner}/{repo}/issues'

    @ responses.activate
    def test_invalid_response_code(self):
        """
        Test for when the request returns an invalid response, i.e. a response with a code other than 200

        Return value should be None, as the request failed
        """
        # Get the mock response body
        regular_body = FileIOForTests.get_regular_body_issues()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=404)

        # Get the result
        result = spider.get_repository_closed_issue_count(
            self.owner, self.repo)

        # The result should be None as the get request failed
        assert result is None

    @ responses.activate
    def test_empty_response_body(self):
        """
        Test for when the request body is empty

        Return value should be None, as there is no way to find the closed issue count
        """
        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body='', status=200)

        # Get the result
        result = spider.get_repository_closed_issue_count(
            self.owner, self.repo)

        # The result should be None as the response had no body, hence no issue count could be found
        assert result is None

    @ responses.activate
    def test_no_closed_issues(self):
        """
        Test for when the request body is not empty, but the closed issue count can not be found

        Return value should be None, as there is no way to find the closed issue count
        """
        # Get the mock response body
        no_closed_body = FileIOForTests.get_no_closed_body_issues()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=no_closed_body, status=200)

        # Get the result
        result = spider.get_repository_closed_issue_count(
            self.owner, self.repo)

        # The result should be None as the closed issue count was not found
        assert result is None

    @responses.activate
    def test_closed_issue_count_found(self):
        """
        Test for when the request body is not empty, and the closed issue count is found

        Return value should be the closed issue count
        """
        # Get the mock response body
        regular_body = FileIOForTests.get_regular_body_issues()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=200)

        # Get the result
        result = spider.get_repository_closed_issue_count(
            self.owner, self.repo)

        # The result should be the closed issue count
        assert result == 8387


class TestIssueRatio:
    """
    Test the get_repository_issue_ratio function.

    We will test the following scenario's:
    1. Both open and closed issue counts are valid numbers
    2. The open issue count is None
    3. The closed issue count is None
    4. Both open and closed issue counts are None
    """

    owner = 'numpy'
    repo = 'numpy'
    url = f'https://github.com/{owner}/{repo}/issues'

    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_open_issue_count', new=mock.Mock(return_value=2026))
    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_closed_issue_count', new=mock.Mock(return_value=8387))
    def test_both_successful(self):
        """
        Test for when both the open and closed issue counts are valid numbers

        Return value should be the actual ratio
        """
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        # The result should be the issue ratio
        assert result == 0.24156432574222012

    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_open_issue_count', new=mock.Mock(return_value=2026))
    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_closed_issue_count', new=mock.Mock(return_value=None))
    def test_open_successful_close_failed(self):
        """
        Test for when the closed issue count is not a valid number

        Return value should be None
        """
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        assert result is None

    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_open_issue_count', new=mock.Mock(return_value=None))
    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_closed_issue_count', new=mock.Mock(return_value=8387))
    def test_open_failed_closed_successful(self):
        """
        Test for when the closed issue count is not a valid number

        Return value should be None
        """
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        assert result is None

    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_open_issue_count', new=mock.Mock(return_value=None))
    @mock.patch('GitHub.github_spider.GitHubSpider.get_repository_closed_issue_count', new=mock.Mock(return_value=None))
    def test_both_failed(self):
        """
        Test for when both the open and closed issue counts are not valid numbers

        Return value should be None
        """
        result = spider.get_repository_issue_ratio(self.owner, self.repo)

        assert result is None
