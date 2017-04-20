import json, logging

from sync.url_parser import URLParser


class Spider:
    """
    The Spider class implements the main crawling functionality.
    """

    def __init__(self):
        """
        Constructor. Simply gets an instance of the URLParser object in
        order to perform the analysis on the links.
        """
        self.url_parser = URLParser()

    def crawl(self, start_url, max_pages, enable_logging=True):
        """
        Implements the crawling functionality: given a starting URL and a maximum
        number of total pages that should be visited, visits every reachable page
        under that domain. Subdomains and domains different from the starting one
        won't be considered. For each page, For each page, the URLs of every static
        asset (images, javascript, stylesheets) are retrieved. Individual results
        are collected as a list of dictionaries and finally returned as a json object.

        :param start_url: the URL from which the crawling starts
        :param max_pages: the maximum number of pages that can be visited
        :param enable_logging: a flag being True if logs should be displayed during the
        crawling, False otherwise.
        :return: a json object containing the URLs visited together with their static
        assets.
        """
        # Feeds the URLParser with the starting URL
        self.url_parser.set_base_url(start_url)
        # Keeps track of the pages that still need to be visited
        pages_to_visit = [start_url]
        # Keeps track of the pages that have been already visited
        already_visited = []

        results = []
        # While there are stil pages that need to be visited and we've not reached
        # the maximum admitted number of visits
        while pages_to_visit and len(already_visited) < max_pages:
            # Gets the first URL and pop it from the queue
            current_url = pages_to_visit.pop(0)
            if enable_logging:
                logging.info('Crawling URL: {}'.format(current_url))
            # If the current URL has not been already visited...
            if current_url not in already_visited:
                # Gets it's static assets and the links that should be subsequently crawled
                static_assets, links_to_follow = self.url_parser.parse_url(current_url)
                if enable_logging:
                    logging.info('Crawled URL: {} - Found {} static assets and {} links to follow'
                                 .format(current_url, len(static_assets), len(static_assets)))
                # Builds up incrementally the results
                results.append({'url': current_url, 'assets': static_assets})
                # Updates the list of pages that should be visited next, and the list of the already
                # visited ones
                pages_to_visit += links_to_follow
                already_visited.append(current_url)
        return json.dumps(results)

