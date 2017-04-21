# Simple Web Crawler

## Problem
Write a simple (not concurrent) web crawler. Given a starting URL, it should visit every reachable
page under that domain, and should not cross subdomains. For example when crawling “www.google.com”
it would not crawl “mail.google.com”. For each page, it should determine the URLs of every static
asset (images, javascript, stylesheets) on that page. The crawler should output to STDOUT in JSON
format listing the URLs of every static asset, grouped by page.
 
For example:

```
[
  {
    "url": "http://www.example.org",
    "assets": [
      "http://www.example.org/image.jpg",
      "http://www.example.org/script.js"
    ]
  },
  {
    "url": "http://www.example.org/about",
    "assets": [
      "http://www.example.org/company_photo.jpg",
      "http://www.example.org/script.js"
    ]
  },
  ..
]
```

## Solution

The solution has been implemented in `python3.5` and it's guaranteed to work on that python version. The project has
been organized into two main folders. The `src` folder contains the `spider` and `url_parser` modules which implement
the crawling logic while the folder `tests` contains the unit tests related to the modules in `src`. Finally the main
of the program is contained in the module `sync_crawler` and it is located at the root level of the project.

### Running the program

The main entry point of the  application is contained in the `sync_crawler.py` module. Simply go into the 
`simple-web-crawler` folder and type:

```aidl
python3 sync_crawler.py -h
```

or alternatively

```aidl
python3 /my/path/to/sync_crawler.py -h
```
to get a usage helper.

Through the helper, you will see the program may take some optional parameters:

- `-m` - `max_pages`: a limit on the maximum number of pages that will be visited by the crawler
- `-l` - `hide_logs`: a flag that allows you to hide logs during crawling
- `-p` - `path_to_file`: the full path to a `json` file in your system where you want to save the results.

If no optional parameter is set, the following defaults will be taken into account:

- `max_pages=5` - meaning that max 5 will be visited
- `hide_logs=False` - meaning that logs will be displayed while crawling
- `path_to_file=None` - meaning that no file will be saved

The final result will be always shown in your terminal.

### Example running

Let's suppose we want to crawl 'https://www.google.it/' for maximum of 5 pages.

```aidl
python3 /my/path/to/sync_crawler.py https://www.google.it/ -m 3
```

Now suppose we want to crawl https://gocardless.com/ for a maximum of 2 pages.

```aidl
python3 /my/path/to/sync_crawler.py https://gocardless.com/ -m 2
```

Finally suppose we want to crawl http://codingnights.com/ for a maximum of 5 pages and
we want to hide the logs of the crawler.

```aidl
python3 /my/path/to/sync_crawler.py https://gocardless.com/ -m 5 -l
```

## Running the tests

The `tests` folder contains two different folders: `static` and `sync`. In the `static` folder
some known results and resources are stored. These resources are used by the `TestCase`s defined
in the `sync` folder. 

To run the tests for the `Spider`, go into the main project folder and type:

```
python3 -m unittest tests/sync/test_spider.py
```

To run the tests for the `URLParser`, go into the main project folder and type:

```
python3 -m unittest tests/sync/url_parser.py
```
