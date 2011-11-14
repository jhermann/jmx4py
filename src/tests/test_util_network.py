""" Network utility tests.
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

import logging
import unittest
import urllib2

from jmx4py.util import network

log = logging.getLogger(__name__)


class SplitURLCredentialsTest(unittest.TestCase):

    def test_simple_url(self):
        url = "http://example.com/"
        self.assertEqual(network.split_url_credentials(url), (url, None, None))


    def test_user_pwd_url(self):
        url = "http://foo:bar@example.com/baz"
        self.assertEqual(network.split_url_credentials(url), ("http://example.com/baz", "foo", "bar"))


    def test_bad_url(self):
        url = "http://foo@example.com/baz"
        self.failUnlessRaises(urllib2.URLError, network.split_url_credentials, url)
