"""
File containing the unit tests for the github_spider.py file.
"""

# Unit testing imports
from unittest import mock

# Import for sending and handling HTTP requests
import responses

# GitHub spider imports
from src.github.github_spider import GitHubSpider

# FileIO import
from tests.unit_tests.spider_tests.file_io import FileIOForGHSpiderTests

# Spider object initialization
spider = GitHubSpider()


class TestUserCount:
    """Class containing the tests for the get_repository_user_count function.

    We will test the following scenario's:
    1. The get request failed:
        - The response code is not 200.
        - The response body is empty.
    2. The get request succeeded but the number of users is not found:
        - The response body is empty.
        - The 'used by' <a> tag is not found.
        - The 'used by' <a> tag has no 'title' attribute.
    3. The get request succeeded and the number of users is found.
    """

    owner = "numpy"
    repo = "numpy"
    url = f"https://github.com/{owner}/{repo}"

    @responses.activate
    def test_invalid_response_code(self) -> None:
        """Test for when the request returns an invalid response.

        i.e. a response with a code other than 200.
        """

        # Get the mock response body
        regular_body = FileIOForGHSpiderTests.get_regular_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=404)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the get request failed
        assert result is None

    @responses.activate
    def test_empty_response_body(self) -> None:
        """Test for when the request body is empty."""

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body="", status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the response had no body, hence no user count could be found
        assert result is None

    @responses.activate
    def test_user_count_tag_not_found(self) -> None:
        """Test for when the request body is not empty but the 'used by' <a> tag can not be found."""

        # Get the mock response body
        no_tag_body = FileIOForGHSpiderTests.get_no_tag_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=no_tag_body, status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the 'used by' <a> tag was not found
        assert result is None

    @responses.activate
    def test_no_title_attribute(self) -> None:
        """Test for when the request body is not empty, and the 'used by' <a> tag is found, but the tag does not have a 'title' attribute."""

        # Get the mock response body
        no_title_body = FileIOForGHSpiderTests.get_no_title_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=no_title_body, status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be None as the 'used by' <a> tag had no 'title' attribute
        assert result is None

    @responses.activate
    def test_user_count_found(self) -> None:
        """Test for when the request body is not empty, and the 'used by' <a> tag is found, and the tag has a 'title' attribute."""

        # Get the mock response body
        regular_body = FileIOForGHSpiderTests.get_regular_body_users()

        # Tell responses to mock the request for us using the provided body and code
        responses.add(responses.GET, self.url, body=regular_body, status=200)

        # Get the result
        result = spider.get_repository_user_count(self.owner, self.repo)

        # The result should be the number of users
        assert result == 975170


"""
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
