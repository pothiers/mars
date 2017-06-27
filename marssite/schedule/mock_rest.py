# see: http://seminar.io/2013/09/27/testing-your-rest-client-in-python/
import urllib.parse 
import os.path

def fake_urlopen(url, timeout=0):
    """
    A stub urlopen() implementation that load json responses from
    the filesystem.
    """
    #!print('DBG fake_urlopen: calling mock_rest.fake_urlopen({})'.format(url))
    try:
        # Map path from url to a file
        parsed_url = urllib.parse.urlparse(url)
        resource_file = os.path.normpath('tests/resources%s' % parsed_url.path)
        # Must return a file-like object
        content = open(resource_file, mode='rb')
    except Exception as err:
        print('DBG fake_urlopen: Error in fake_urlopen({}); {}'.format(url, err))
        content = None
    #print('DBG fake_urlopen: content={}'.format(content))
    return content


