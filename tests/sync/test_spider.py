import json
from unittest import TestCase, main
from unittest.mock import patch

import tests.sync.mocks as mocks
from src.sync.spider import Spider


class TestSpider(TestCase):
    """
    Collection of test cases for the Spider class.
    """

    @patch('src.sync.url_parser.URLParser.parse_url', side_effect=mocks.mocked_parser)
    def test_crawl_one(self, mock_parse_url):
        """
        Tests the crawl method for max_urls=1.
        """
        spider = Spider()
        current_json_response = spider.crawl('http://www.sample.com/', 1)
        expected_json_response = json.dumps([{'url': 'http://www.sample.com/',
                                              'assets': ['https://www.sample.com/some_img.png']}])
        self.assertEqual(current_json_response, expected_json_response)
        del spider

    @patch('src.sync.url_parser.URLParser.parse_url', side_effect=mocks.mocked_parser)
    def test_crawl_two(self, mock_parse_url):
        """
        Tests the crawl method for max_urls=2.
        """
        spider = Spider()
        current_json_response = spider.crawl('http://www.sample.com/', 2)
        expected_json_response = json.dumps([{'url': 'http://www.sample.com/',
                                              'assets': ['https://www.sample.com/some_img.png']},
                                             {'url': 'http://www.sample.com/test1/',
                                              'assets': ['https://www.sample.com/some_img.png',
                                                         'https://www.sample.com/some_img1.png']}])
        self.assertEqual(current_json_response, expected_json_response)
        del spider

    @patch('src.sync.url_parser.URLParser.parse_url', side_effect=mocks.mocked_parser)
    def test_crawl_three(self, mock_parse_url):
        """
        Tests the crawl method for max_urls=3.
        """
        spider = Spider()
        current_json_response = spider.crawl('http://www.sample.com/', 3)
        expected_json_response = json.dumps([{'url': 'http://www.sample.com/',
                                              'assets': ['https://www.sample.com/some_img.png']},
                                             {'url': 'http://www.sample.com/test1/',
                                              'assets': ['https://www.sample.com/some_img.png',
                                                         'https://www.sample.com/some_img1.png']},
                                             {'url': 'http://www.sample.com/test2/',
                                              'assets': ['https://www.sample.com/some_img2.png']}])
        self.assertEqual(current_json_response, expected_json_response)
        del spider


if __name__ == '__main__':
    main()
