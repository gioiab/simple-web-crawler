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
    def __init__(self, data, status_code, headers={}):
        self.data = data
        self.status_code = status_code
        self.headers = headers


def mocked_http_request(*args, **kwargs):
    """
    This method is used to mock urllib.request.Request objects.

    :param args: positional parameters
    :param kwargs: keyword arguments
    :return: the mocked request
    """
    return MockHTTPRequest(args[0], kwargs['method'])


def mocked_http_response_get(*args):
    """
    This method is used by the mock to replace urllib.request.urlopen.

    :param args: the input arguments of the urllib.request.urlopen call.
    :return: the mocked response
    """
    mock_request = args[0]
    assert isinstance(mock_request, MockHTTPRequest)
    if mock_request.url == 'http://someurl.com/test':
        return MockHTTPResponse("<html><body><a href='http://www.sample.com/test'></a></html>", 200)
    else:
        return MockHTTPResponse("<html><body><a href='http://www.sample.com/other'></a></html>", 200)

    return MockResponse({}, 404)


def mocked_parser(*args):
    """
    This method is used by the mock to replace the URLParser object.

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
