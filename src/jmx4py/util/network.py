""" Networking.

    @author: jhe
"""
#   Copyright 2011 Juergen Hermann
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import urllib2
import urlparse


class RetryLimitingHTTPPasswordMgrWithDefaultRealm(urllib2.HTTPPasswordMgrWithDefaultRealm):
    """ Fixes http://bugs.python.org/issue8797 for certain Python versions provided by Linux packaging
        and still running in the wild.
    """
    retries = 0

    def find_user_password(self, realm, authuri):
        """ Limit number of queries per request.

            Note that retries needs to be reset in the calling code.
        """
        # allow sending the username:password 5 times before failing!
        if self.retries > 5:
            from httplib import HTTPMessage
            from StringIO import StringIO
            raise urllib2.HTTPError(authuri, 401, "basic auth failed for realm %r" % realm,
                HTTPMessage(StringIO("")), None)

        self.retries += 1
        return urllib2.HTTPPasswordMgrWithDefaultRealm.find_user_password(self, realm, authuri)


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


def urlopen(req, username=None, password=None):
    """ C{urlopen()} wrapper supporting Basic Auth credentials.

        @param req: to be opened.
        @param username: Optional default credentials.
        @param password: Optional default credentials.
        @return: Handle for C{url}.
    """
    # Get URL from request object, else treat it as a string
    try:
        urlstr = req.get_full_url()
    except AttributeError:
        urlstr = req

    # Try to get credentials from the URL
    credentials = None
    _, url_username, url_password = split_url_credentials(urlstr)
    if url_username:
        username, password = url_username, url_password

    if username or password:
        # Register opener
        credentials = (username, password)
        if credentials not in urlopen.opener:
            urlopen.pwd_mgr[credentials] = RetryLimitingHTTPPasswordMgrWithDefaultRealm()
            urlopen.handler[credentials] = urllib2.HTTPBasicAuthHandler(urlopen.pwd_mgr[credentials])
            urlopen.opener[credentials] = urllib2.build_opener(
                urlopen.handler[credentials],
                urllib2.HTTPHandler(debuglevel=int(urlopen.debug)),
                urllib2.HTTPSHandler(debuglevel=int(urlopen.debug)),
            )

        # Add credentials entry for Python >= 2.4, and reset retry counter
        urlopen.pwd_mgr[credentials].add_password(None, urlstr, username, password)
        urlopen.pwd_mgr[credentials].retries = 0
        urlopen.handler[credentials].retried = 0 # fix Python 2.6.6 bug
    elif credentials not in urlopen.opener:
        # Opener for public URLs
        urlopen.opener[credentials] = urllib2.build_opener(
            urllib2.HTTPHandler(debuglevel=int(urlopen.debug)),
            urllib2.HTTPSHandler(debuglevel=int(urlopen.debug)),
        )

    # Open URL and return handle
    return urlopen.opener[credentials].open(req)

urlopen.opener = {}
urlopen.handler = {}
urlopen.pwd_mgr = {}
urlopen.debug = False
