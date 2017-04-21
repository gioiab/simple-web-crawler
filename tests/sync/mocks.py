import urllib.error

class MockHTTPRequest:
    """
    Defines the mock for a generic urllib.request.Request.
    """
    def __init__(self, url, method):
        self.url = url
        self.method = method


class MockHTTPResponse:
    """
    Defines the mock for a generic urlopen response.
    """
    def __init__(self, url, data, status_code, headers={}):
        self.url = url
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def read(self):
        return self.data

    def geturl(self):
        return self.url

    def info(self):
        return self.headers


def mocked_http_request(*args, **kwargs):
    """
    This method is used to mock urllib.request.Request objects.

    :param args: positional parameters
    :param kwargs: keyword arguments
    :return: the mocked request
    """
    return MockHTTPRequest(args[0], kwargs['method'])


def mocked_http_response(*args):
    """
    This method is used by the mock to replace urllib.request.urlopen.

    :param args: the input arguments of the urllib.request.urlopen call
    :return: the mocked response
    """
    mock_request = args[0]
    assert isinstance(mock_request, MockHTTPRequest)
    if mock_request.url == 'http://someurl.com/test' and mock_request.method == 'GET':
        return MockHTTPResponse('http://someurl.com/test',
                                "<html><body><a href='http://someurl.com/other'></a></body></html>",
                                200,
                                {'Content-Type': 'text/html'})
    elif mock_request.url == 'http://someotherurl.com/test' and mock_request.method == 'GET':
        return MockHTTPResponse('http://someotherurl.com/test',
                                "<html><body><a href='http://someotherurl.com/other'></a></body></html>",
                                200,
                                {'Content-Type': 'text/html'})
    elif mock_request.url == 'http://someurl.com/test' and mock_request.method == 'HEAD':
        return MockHTTPResponse('http://someurl.com/test', "", 200, {'Content-Type': 'text/html'})
    elif mock_request.url == 'http://someotherurl.com/test.png' and mock_request.method == 'HEAD':
        return MockHTTPResponse('http://someotherurl.com/test.png', "", 200, {'Content-Type': 'image/png'})
    elif mock_request.method == 'GET' or mock_request.method == 'HEAD':
        # Other URLs but always GET method
        return MockHTTPResponse(mock_request.url, "<html><body>404 Error<body></html>",
                                404, {'Content-Type': 'text/html'})
    else:
        return MockHTTPResponse(mock_request.url, "<html><body>500 Internal Server Error</body></html>",
                                500, {'Content-Type': 'text/html'})


def mocked_get_valid_linked_urls(*args):
    """
    This method is used to mock the _get_valid_linked_urls method of the URLParser object.

    :param args: the input arguments
    :return: the mocked response
    """
    response = args[0]
    if response == "<html><body><a href='http://someurl.com/other'></a></body></html>":
        return ['http://someurl.com/other']
    elif response == "<html><body><a href='http://someotherurl.com/other'></a></body></html>":
        return ['http://someotherurl.com/other']
    elif response == "<html><body>404 Error<body></html>":
        return []
    else:  # response == "<html><body>500 Internal Server Error</body></html>":
        return []


def mocked_get_assets(*args):
    """
    This method is used to mock the _get_assets method of the URLParser object.

    :param args: the input arguments
    :return: the mocked response
    """
    response = args[0]
    if response == "<html><body><a href='http://someurl.com/other'></a></body></html>":
        return [], ['http://someurl.com/other']
    elif response == "<html><body><a href='http://someotherurl.com/other'></a></body></html>":
        return [], ['http://someotherurl.com/other']
    elif response == "<html><body>404 Error<body></html>":
        return [], []
    else:  # response == "<html><body>500 Internal Server Error</body></html>":
        return [], []


def mocked_parse_url(*args):
    """
    This method is used to mock the parse_url method of the URLParser object.

    :param args: the input arguments
    :return: the mocked object
    """
    url = args[0]
    static_assets = []
    links_to_follow = []
    if url == 'http://www.sample.com/':
        static_assets = ['https://www.sample.com/some_img.png']
        links_to_follow = ['http://www.sample.com/test1/', 'http://www.sample.com/test2/']
    elif url == 'http://www.sample.com/test1/':
        static_assets = ['https://www.sample.com/some_img.png', 'https://www.sample.com/some_img1.png']
    elif url == 'http://www.sample.com/test2/':
        static_assets = ['https://www.sample.com/some_img2.png']
    return static_assets, links_to_follow
