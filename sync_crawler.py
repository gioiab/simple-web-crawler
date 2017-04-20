import argparse
import logging
import time

from src.sync.spider import Spider


def main():
    """
    Main function of the program. Provides command line facilities to crawl websites
    using a simple synchronous web crawler.
    """
    # Acquires input arguments from the user
    parser = argparse.ArgumentParser(description='A simple synchronous web crawler')
    parser.add_argument('website', help='the website you want to start the crawling from')
    parser.add_argument('-m', dest='max_pages', type=int, default=5,
                        help='the maximum number of pages that will be visited')
    parser.add_argument('-l', dest='show_logs', type=bool, default=True,
                        help='a flag that tells if logs should be shown')
    parser.add_argument('-s', dest='path_to_file', type=str,
                        help='tells if the results should be saved to file and provides the full path for saving')
    args = parser.parse_args()
    # Sets up the main Logger of the program to the INFO level, this means that everything with a severity
    # greater than or equal to the INFO level will be shown (e.g.: warnings, errors)
    logging.getLogger().setLevel(logging.INFO)
    # Storing the current time
    start_time = time.time()
    # Setting up the Spider for crawling
    spider = Spider()
    result = spider.crawl(args.website, args.max_pages, args.show_logs)
    print('Result of the crawling for {} returned in {:.2f} seconds:'.format(args.website, time.time()-start_time))
    print(result)
    # In addition, saves the result to a file if needed
    if args.path_to_file:
        with open(args.path_to_file, 'w') as outfile:
            # Result is already a json string!
            outfile.write(result)
    # Cleans up the environment deleting spider
    del spider

if __name__ == '__main__':
    """
    Main entry point of the program. Simply calls the main function.
    """
    main()

