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