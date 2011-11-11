""" Networking. 

    @author: jhe
"""
import urllib2
import urlparse


def split_url_credentials(url):
    """ Split username and password from an URL and return tuple
        (plain_url, username, password). 
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    username, password = None, None

    if '@' in netloc:
        try:
            credentials, netloc = netloc.split('@', 1)
            username, password = credentials.split(':', 1)
        except (TypeError, ValueError), exc:
            raise urllib2.URLError("Malformed URL credentials in %r (%s)" % (url, exc))

        url = urlparse.urlunsplit((scheme, netloc, path, query, fragment))

    return url, username, password


