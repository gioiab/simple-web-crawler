import logging
from lxml import html
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from urllib.parse import urljoin, urlsplit


class URLParser:
    """
    The URLParser class provides utilities to parse a web page, extract
    its links, and classify them as static or non-static assets.
    """

    def __init__(self, enable_logging=True):
        """
        Constructor. Mainly initializes the base_url variable. This variable
        will be used to avoid returning subdomains of the original domain.
        """
        self.base_url = None
        self.enable_logging = enable_logging

    def set_base_url(self, base_url):
        """
        Sets the base URL in order not to return subdomains.

        :param base_url: the URL that will be taken as baseline
        """
        self.base_url = base_url

    def is_a_valid_url(self, url):
        """
        Determines if a URL is valid or not. An input URL is defined to be valid if it's
        network location part is equal to the one of the base_url.

        :param url: the input URL that needs to be validated
        :return: True if the URL is valid, False otherwise
        """
        base_url_split = urlsplit(self.base_url)
        current_url_split = urlsplit(url)
        # The following doesn't take into account the scheme when checking the validity and checks
        # that the two network location paths are equal. The path part should not be equal in order
        # to discard urls which are completely equal to the base one
        return current_url_split.netloc == base_url_split.netloc and base_url_split.path != current_url_split.path

    def get_valid_linked_urls(self, page):
        """
        Given a HTML page as a string, gets all the valid linked URLs in it.

        :param page: an HTML page as a string
        :return: all the valid linked URLs contained in the page
        """
        # Gets all the link within the page with lxml
        links = html.iterlinks(page)
        # Merges the base_url with each url found in the page to bring relative URLs to absolute
        # Note: absolute URLs won't be affected, they will stay the same
        linked_urls = [urljoin(self.base_url, link[2]) for link in links]
        # Filters and gets only the valid URLs
        valid_linked_urls = [linked_url for linked_url in linked_urls if self.is_a_valid_url(linked_url)]
        return valid_linked_urls

    def get_assets(self, page):
        """
        Given an HTML page as a string, returns its static and non-static assets.

        :param page: an HTML page as a string
        :return: the tuple (static_assets, links_to_follow) where the former element represents the
        list of static assets found while the latter is a list of non-static assets found in the page.
        """
        valid_linked_urls = self.get_valid_linked_urls(page)
        static_assets = []
        links_to_follow = []
        # Checks what a valid URLs contains by sending HEAD requests...
        for valid_url in valid_linked_urls:
            request = Request(valid_url, method="HEAD")
            try:
                response = urlopen(request)
                # Gets the real URL in case of redirect
                actual_url = response.geturl()
                if 'text/html' in response.info()['Content-Type']:
                    links_to_follow.append(actual_url)
                else:
                    static_assets.append(actual_url)
            except HTTPError as http_err:
                logging.error('HTTPError returned in sending a HEAD request to {} - HTTP code {}'
                              .format(actual_url, http_err.code))
                continue
        return static_assets, links_to_follow

    def parse_url(self, url):
        """
        Parse the HTML content of the current URL in order to find static and non-static assets.

        :param url: the URL for which the page should be fetched and static/non-static assets
        should be determined
        :return: the tuple (static_assets, links_to_follow) where the former element represents the
        list of static assets found while the latter is a list of non-static assets found in the page.
        """
        try:
            # Fetches the page at the given URL in a synchronous way
            page = urlopen(url).read().decode("utf-8")
        except HTTPError as http_err:
            if self.enable_logging:
                logging.error('HTTPError returned in fetching the content for {} - HTTP code {}'
                              .format(url, http_err.code))
            return [], []
        except URLError as url_err:
            if self.enable_logging:
                logging.error('URLError returned for {}'.format(url))
                logging.error(url_err)
            return [], []
        else:
            # Gets the assets of the page
            return self.get_assets(page)
