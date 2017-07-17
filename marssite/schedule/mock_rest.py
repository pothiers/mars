# see: http://seminar.io/2013/09/27/testing-your-rest-client-in-python/
import urllib.parse 
import os.path

def fake_urlopen(url, timeout=0):
    """
    A stub urlopen() implementation that load json responses from
    the filesystem.
    """
    #!print('Using mock_rest.fake_urlopen({})'.format(url))
    try:
        # Map path from url to a file
        parsed_url = urllib.parse.urlparse(url)
        #print('DBG parsed_url={}'.format(parsed_url))
        #!resource_file = os.path.normpath('tests/resources%s' % parsed_url.path)
        resource_file = os.path.normpath('tests/resources{}/{}'
                                         .format(parsed_url.path, parsed_url.query))
        # Must return a file-like object
        #!print('DBG resource_file={}'.format(resource_file))
        content = open(resource_file, mode='rb')
    except Exception as err:
        print('DBG fake_urlopen: Error in fake_urlopen({}); file={}, {}'
              .format(url, resource_file, err))
        content = None
    #print('DBG fake_urlopen: content={}'.format(content))
    return content


