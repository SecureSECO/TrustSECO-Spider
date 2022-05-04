"""
File containing the unit tests for the cve_spider.py file.
"""

import bs4
import pytest
from unittest import mock
import responses
from bs4 import BeautifulSoup
from CVE.cve_spider import CVESpider


class TestVulnerabilityCount:
    """
    Class for testing the get_cve_vulnerability_count function.

    We will test for the following possible return values of get_cve_codes:
    1. None
    2. Empty list
    3. Non-empty list
    """

    @pytest.mark.parametrize('return_value, expected_value', [(None, None), ([], 0), (['CVE-2019-1234', 'CVE-2019-1235'], 2)])
    def test_all(self, return_value, expected_value):
        """
        This function will test all of the possible scenarios using mocking to change the output of the get_cve_codes function.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        with mock.patch('CVE.cve_spider.CVESpider.get_cve_codes', return_value=return_value):
            # Call the get_cve_vulnerability_count function
            result = cve_spider.get_cve_vulnerability_count('test_package')

            # Check the result
            assert result == expected_value


class TestGetAllCVEData:
    """
    Class for testing the get_all_cve_data function.

    We will test for the following possible return values of get_cve_codes:
    1. None
    2. Empty list
    3. Non-empty list

    We will also test for the following possible return values of extract_cve_data:
    1. None
    2. Actual object
    """

    @pytest.mark.parametrize('get_cve_codes_rv', [None, [], ['CVE-2019-1234', 'CVE-2019-1235']])
    @pytest.mark.parametrize('extract_cve_data_rv', [None, {'test_key': 'test_value'}])
    def test_all(self, get_cve_codes_rv, extract_cve_data_rv):
        """
        This function will test all of the possible scenarios using mocking to change the output of the get_cve_codes and extract_cve_data functions.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Mock the get_cve_codes function
        with mock.patch('CVE.cve_spider.CVESpider.get_cve_codes', return_value=get_cve_codes_rv):
            # If get_cve_codes returns None, then the output should also be None
            if get_cve_codes_rv is None:
                assert cve_spider.get_all_cve_data('test_package') is None
            # Else, if get_cve_codes returns an empty list, then the output should also be an empty list
            elif get_cve_codes_rv == []:
                assert cve_spider.get_all_cve_data('test_package') == []
            # Else, if get_cve_codes returns a non-empty list, then the output can differ depending on the value of extract_cve_data
            else:
                # Mock the extract_cve_data function
                with mock.patch('CVE.cve_spider.CVESpider.extract_cve_data', return_value=extract_cve_data_rv):
                    # If extract_cve_data returns only None, then the output list should have no elements
                    if extract_cve_data_rv is None:
                        assert cve_spider.get_all_cve_data(
                            'test_package') == []
                    # Else, if extract_cve_data returns an object every time, then the output list should have the same number of objects as the number of CVE codes, and those objects should be the given object
                    else:
                        # Create the expected list of data
                        expected = []
                        for cve_code in get_cve_codes_rv:
                            expected.append(extract_cve_data_rv)

                        assert cve_spider.get_all_cve_data(
                            'test_package') == expected


class TestExtractData:
    """
    Class for testing the extract_cve_data function.

    We will test the following scenarios:
    The html contains:
    1. Nothing
    2. Only the score
    3. Only the affected versions
    4. Only a broken affected versions object
    5. Everything
    """

    def test_empty_page(self):
        """
        Function for testing the scenario where the html page is empty.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=None):
            # Call the extract_cve_data function
            result = cve_spider.extract_cve_data('test_cve_code')

            # Check the result
            assert result is None

    def test_no_version_page(self):
        """
        Function for testing the scenario where the html page contains only the score.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_no_version_page_extract(), 'html.parser')

        print('test')

        # Set the expected return value
        expected_cve_data = {
            'CVE_ID': 'test_cve_code',
            'CVE_score': 7.5,
            'CVE_affected_version_start_type': None,
            'CVE_affected_version_start': None,
            'CVE_affected_version_end_type': None,
            'CVE_affected_version_end': None,
        }

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the extract_cve_data function
            result = cve_spider.extract_cve_data('test_cve_code')

            # Check the result
            assert result == expected_cve_data

    def test_incorrect_version_page(self):
        """
        Function for testing the scenario where the html page contains a version object, but with missing information.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_incorrect_version_page_extract(), 'html.parser')

        print('test')

        # Set the expected return value
        expected_cve_data = {
            'CVE_ID': 'test_cve_code',
            'CVE_score': 7.5,
            'CVE_affected_version_start_type': None,
            'CVE_affected_version_start': None,
            'CVE_affected_version_end_type': None,
            'CVE_affected_version_end': None,
        }

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the extract_cve_data function
            result = cve_spider.extract_cve_data('test_cve_code')

            # Check the result
            assert result == expected_cve_data

    def test_no_score_page(self):
        """
        Function for testing the scenario where the html page contains only the vulnerable versions.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_no_score_page_extract(), 'html.parser')

        print('test')

        # Set the expected return value
        expected_cve_data = {
            'CVE_ID': 'test_cve_code',
            'CVE_score': None,
            'CVE_affected_version_start_type': None,
            'CVE_affected_version_start': None,
            'CVE_affected_version_end_type': 'excluding',
            'CVE_affected_version_end': '1.19.0',
        }

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the extract_cve_data function
            result = cve_spider.extract_cve_data('test_cve_code')

            # Check the result
            assert result == expected_cve_data

    def test_regular_page(self):
        """
        Function for testing the scenario where the html page contains all the wanted information.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_regular_page_extract(), 'html.parser')

        print('test')

        # Set the expected return value
        expected_cve_data = {
            'CVE_ID': 'test_cve_code',
            'CVE_score': 7.5,
            'CVE_affected_version_start_type': None,
            'CVE_affected_version_start': None,
            'CVE_affected_version_end_type': 'excluding',
            'CVE_affected_version_end': '1.19.0',
        }

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the extract_cve_data function
            result = cve_spider.extract_cve_data('test_cve_code')

            # Check the result
            assert result == expected_cve_data


class TestGetParseWebsite:
    """
    Class for testing the get_and_parse_webpage function

    To test this function, we will test the following scenarios:
    1. Invalid url
    2. Invalid return code
    3. Valid request
    """

    @pytest.mark.parametrize('given_url, expected_value', [(None, None), ('', None), ('test_url', None), ('google.com', None)])
    def test_invalid_url(self, given_url, expected_value):
        """
        Function for testing the scenario where the url is invalid.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Run the function
        result = cve_spider.get_and_parse_webpage(given_url)

        # Make sure the result matches what we expect
        assert expected_value is result

    @ responses.activate
    def test_invalid_return_code(self):
        """
        Function for testing the scenario where the return code is invalid.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Set the url
        url = 'https://google.com'

        # Add the url to the responses list
        responses.add(responses.GET, url, status=404)

        # Run the function
        result = cve_spider.get_and_parse_webpage(url)

        assert result is None

    @ responses.activate
    def test_valid_request(self):
        """
        Function for testing the scenario where the html is invalid.
        """
        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Set the url
        url = 'https://google.com'

        # Add the url to the responses list
        responses.add(responses.GET, url,
                      body='<html></html>', status=200)

        # Run the function
        result = cve_spider.get_and_parse_webpage(url)

        assert type(result) is bs4.BeautifulSoup


class TestGetCVECodes:
    """
    Class for testing the get_cve_codes function

    We will be testing for the following scenarios:
    1. The returned soup is None
    2. There are no table tags
    3. The wanted table tag does not exist
    4. There are no links in the table
    5. Valid site
    """

    def test_soup_is_none(self):
        """
        Function for testing the scenario where the soup is None.
        """

        # Initialise the CVESpider object
        cve_spider = CVESpider()

        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=None):
            # Call the function
            result = cve_spider.get_cve_codes('')

            # Check the result
            assert result is None

    def test_no_tables(self):
        """
        Function for testing the scenario where there are no table tags.
        """

        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_no_tables_page_get_codes(), 'html.parser')

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the function
            result = cve_spider.get_cve_codes('')

            # Check the result
            assert result is None

    def test_missing_table(self):
        """
        Function for testing the scenario where the wanted table tag does not exist.
        """

        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_missing_table_page_get_codes(), 'html.parser')

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the function
            result = cve_spider.get_cve_codes('')

            # Check the result
            assert result is None

    def test_no_links(self):
        """
        Function for testing the scenario where there are no link tags within the table
        """

        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_no_links_page_get_codes(), 'html.parser')

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the function
            result = cve_spider.get_cve_codes('')

            # Check the result
            assert result == []

    def test_valid_page(self):
        """
        Function for testing the scenario where the received html page is completely valid
        """

        # Initialise the CVESpider object
        cve_spider = CVESpider()

        # Create the soup object
        soup = BeautifulSoup(
            FileIOForCVETests.get_regurlar_page_get_codes(), 'html.parser')

        # Set the expected value
        expected_value = [
            'CVE-2021-41496',
            'CVE-2021-41495',
            'CVE-2021-34141',
            'CVE-2021-33430',
            'CVE-2019-6446',
            'CVE-2017-12852',
            'CVE-2014-1859',
            'CVE-2014-1858',
        ]

        # Mock the get_and_parse_webpage function
        with mock.patch('CVE.cve_spider.CVESpider.get_and_parse_webpage', return_value=soup):
            # Call the function
            result = cve_spider.get_cve_codes('')

            # Check the result
            assert result == expected_value


class FileIOForCVETests:
    """
    Class that contains all of the IO functions for the tests.
    """

    def get_regular_page_extract():
        with open('tests/test_files/cve_spider_extract/regular_vulnerability_page.txt', 'r', encoding='iso-8859-15') as regular:
            regular_body = regular.read()
        return regular_body

    def get_no_version_page_extract():
        with open('tests/test_files/cve_spider_extract/no_version_vulnerability_page.txt', 'r', encoding='iso-8859-15') as no_version:
            no_version_body = no_version.read()
        return no_version_body

    def get_no_score_page_extract():
        with open('tests/test_files/cve_spider_extract/no_score_vulnerability_page.txt', 'r', encoding='iso-8859-15') as no_score:
            no_score_body = no_score.read()
        return no_score_body

    def get_incorrect_version_page_extract():
        with open('tests/test_files/cve_spider_extract/incorrect_version_vulnerability_page.txt', 'r', encoding='iso-8859-15') as incorrect_version:
            incorrect_version_body = incorrect_version.read()
        return incorrect_version_body

    def get_regurlar_page_get_codes():
        with open('tests/test_files/cve_spider_get_codes/regular_page.txt', 'r', encoding='iso-8859-15') as regular:
            regular_body = regular.read()
        return regular_body

    def get_no_tables_page_get_codes():
        with open('tests/test_files/cve_spider_get_codes/no_tables_page.txt', 'r', encoding='iso-8859-15') as no_tables:
            no_tables_body = no_tables.read()
        return no_tables_body

    def get_no_links_page_get_codes():
        with open('tests/test_files/cve_spider_get_codes/no_links_page.txt', 'r', encoding='iso-8859-15') as no_links:
            no_links_body = no_links.read()
        return no_links_body

    def get_missing_table_page_get_codes():
        with open('tests/test_files/cve_spider_get_codes/missing_table_page.txt', 'r', encoding='iso-8859-15') as missing_table:
            missing_table_body = missing_table.read()
        return missing_table_body
