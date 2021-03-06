import os
from unittest import TestCase, main
from unittest.mock import patch

import tests.sync.mocks as mocks
from src.sync.url_parser import URLParser
from tests.static.known_results import VALID_URLS_IN_GOOGLE_HOME, VALID_URLS_IN_SAMPLE_HOME


class TestURLParser(TestCase):
    """
    Collection of test cases for the URLParser class.
    """

    def assert_raise_with_msg(self, error, error_message, f, *args):
        """
        Checks that the given error/exception is thrown along with the given error_message when f is executed.

        :param error: the exception that should be raised
        :param error_message: the expected error message
        :param f: the function raising the exception
        :param args: the function arguments
        """
        with self.assertRaises(error) as context:
            f(*args)
        self.assertTrue(error_message in str(context.exception))

    @staticmethod
    def get_sample_parser(base_url):
        """
        Utility class to get a parser for test cases.

        :param base_url: the base URL with which the parser should be fed
        :return: the instance of the sample parser
        """
        parser = URLParser()
        parser.set_base_url(base_url)
        return parser

    def test_creation(self):
        """
        Tests the creation of an URLPaser.
        """
        parser = URLParser()
        self.assertEqual(parser.base_url, None)
        del parser

    def test_set_base_url(self):
        """
        Tests the set_base_url method of the parser.
        """
        parser = URLParser()
        parser.set_base_url('https://www.google.it/')
        self.assertEqual(parser.base_url, 'https://www.google.it/')
        del parser

    def test_is_valid_url_with_missing_base_url(self):
        """
        Tests the _is_a_valid_url method when no base_url has been previously fed to the parser.
        """
        parser = URLParser()
        self.assertEqual(parser.base_url, None)
        self.assert_raise_with_msg(ValueError,
                                   'Base URL not set before asking to parse the content of https://www.google.it/.',
                                   parser._is_a_valid_url, 'https://www.google.it/')
        parser.set_base_url('')
        self.assertEqual(parser.base_url, '')
        self.assert_raise_with_msg(ValueError,
                                   'Base URL not set before asking to parse the content of https://www.google.it/.',
                                   parser._is_a_valid_url, 'https://www.google.it/')
        del parser

    def test_is_a_valid_url(self):
        """
        Tests the is_a_valid_url method when a base_url has been previously fed to the parser.
        """
        parser = self.get_sample_parser('https://www.google.it/')
        self.assertTrue(parser._is_a_valid_url('https://www.google.it/test'))
        # Subdomains should not be valid
        self.assertFalse(parser._is_a_valid_url('https://plus.google.it/'))
        del parser

    def template_test_get_valid_linked_urls(self, base_url, path_to_sample_html, known_valid_urls):
        """
        Base class for testing the method _get_valid_linked_urls.

        :param base_url: the base URL with which the parser should be fed
        :param path_to_sample_html: the path to a sample HTML page
        :param known_valid_urls: a list of known valid URL for the sample page
        """
        parser = self.get_sample_parser(base_url)
        with open(path_to_sample_html, 'r') as sample_home_html:
            sample_home_str = sample_home_html.read()
            self.assertEqual(parser._get_valid_linked_urls(sample_home_str), known_valid_urls)
        del parser

    def test_get_valid_linked_urls(self):
        """
        Tests the _get_valid_linked_urls method on knwon samples.
        """
        current_file_path = os.path.dirname(os.path.realpath(__file__))
        path_to_static_folder = os.path.join(current_file_path, '../static')
        self.template_test_get_valid_linked_urls('https://www.google.it/',
                                                 os.path.join(path_to_static_folder, 'google.html'),
                                                 VALID_URLS_IN_GOOGLE_HOME)
        self.template_test_get_valid_linked_urls('https://www.sample.com/',
                                                 os.path.join(path_to_static_folder, 'sample.html'),
                                                 VALID_URLS_IN_SAMPLE_HOME)

    @patch('urllib.request.Request', side_effect=mocks.mocked_http_request)
    @patch('urllib.request.urlopen', side_effect=mocks.mocked_http_response)
    def test_send_http_request(self, mock_req, mock_resp):
        """
        Tests the _send_http_request method.
        """
        # Tests successful GETs
        response = URLParser._send_http_request('http://someurl.com/test', method="GET")
        self.assertEqual(response.url, 'http://someurl.com/test')
        self.assertEqual(response.data, "<html><body><a href='http://someurl.com/other'></a></body></html>")
        self.assertEqual(response.status_code, 200)
        response = URLParser._send_http_request('http://someotherurl.com/test', method="GET")
        self.assertEqual(response.url, 'http://someotherurl.com/test')
        self.assertEqual(response.data, "<html><body><a href='http://someotherurl.com/other'></a></body></html>")
        self.assertEqual(response.status_code, 200)
        # Tests 404
        response = URLParser._send_http_request('http://errorurl.com/', method="GET")
        self.assertEqual(response.url, 'http://errorurl.com/')
        self.assertEqual(response.data, "<html><body>404 Error<body></html>")
        self.assertEqual(response.status_code, 404)
        # Tests successful HEADs
        response = URLParser._send_http_request('http://someurl.com/test', method="HEAD")
        self.assertEqual(response.url, 'http://someurl.com/test')
        self.assertEqual(response.data, "")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/html')
        response = URLParser._send_http_request('http://someotherurl.com/test.png', method="HEAD")
        self.assertEqual(response.url, 'http://someotherurl.com/test.png')
        self.assertEqual(response.data, "")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/png')
        # Tests 404 HEAD
        response = URLParser._send_http_request('http://errorurl.com/', method="HEAD")
        self.assertEqual(response.url, 'http://errorurl.com/')
        self.assertEqual(response.data, "<html><body>404 Error<body></html>")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'text/html')
        # Tests different request types
        response = URLParser._send_http_request('http://errorurl.com/', method="PUT")
        self.assertEqual(response.url, 'http://errorurl.com/')
        self.assertEqual(response.data, "<html><body>500 Internal Server Error</body></html>")
        self.assertEqual(response.status_code, 500)

    @patch('src.sync.url_parser.URLParser._get_valid_linked_urls', side_effect=mocks.mocked_get_valid_linked_urls)
    @patch('urllib.request.Request', side_effect=mocks.mocked_http_request)
    @patch('urllib.request.urlopen', side_effect=mocks.mocked_http_response)
    def test_get_assets(self, mock_urls, mock_req, mock_resp):
        """
        Tests the _get_assets method.
        """
        parser = self.get_sample_parser('http://someurl.com/')
        assets = parser._get_assets("<html><body><a href='http://someurl.com/other'></a></body></html>")
        self.assertEqual(assets[0], [])
        self.assertEqual(assets[1], ['http://someurl.com/other'])
        assets = parser._get_assets("<html><body><a href='http://someotherurl.com/other'></a></body></html>")
        self.assertEqual(assets[0], [])
        self.assertEqual(assets[1], ['http://someotherurl.com/other'])
        assets = parser._get_assets("<html><body>404 Error<body></html>")
        self.assertEqual(assets[0], [])
        self.assertEqual(assets[1], [])
        del parser

    @patch('urllib.request.Request', side_effect=mocks.mocked_http_request)
    @patch('urllib.request.urlopen', side_effect=mocks.mocked_http_response)
    @patch('src.sync.url_parser.URLParser._get_assets', side_effect=mocks.mocked_get_assets)
    def test_parse_url(self, mock_req, mock_resp, mock_assets):
        """
        Tests the _parse_url method.
        """
        parser = self.get_sample_parser('http://someurl.com/')
        static_assets, links_to_follow = parser.parse_url('http://someurl.com/test')
        self.assertEqual(static_assets, [])
        self.assertEqual(links_to_follow, ['http://someurl.com/other'])
        parser.set_base_url('http://someotherurl.com/')
        static_assets, links_to_follow = parser.parse_url('http://someotherurl.com/test')
        self.assertEqual(static_assets, [])
        self.assertEqual(links_to_follow, ['http://someotherurl.com/other'])
        static_assets, links_to_follow = parser.parse_url('http://errorurl.com/')
        self.assertEqual(static_assets, [])
        self.assertEqual(links_to_follow, [])
        del parser

    def test_parse_url_with_missing_base_url(self):
        """
        Tests the parse_url method when no base_url has been previously fed to the parser.
        """
        parser = URLParser()
        self.assertEqual(parser.base_url, None)
        self.assert_raise_with_msg(ValueError,
                                   'Base URL not set before asking to parse the content of https://www.google.it/.',
                                   parser.parse_url, 'https://www.google.it/')
        parser.set_base_url('')
        self.assertEqual(parser.base_url, '')
        self.assert_raise_with_msg(ValueError,
                                   'Base URL not set before asking to parse the content of https://www.google.it/.',
                                   parser.parse_url, 'https://www.google.it/')
        del parser

if __name__ == '__main__':
    main()
