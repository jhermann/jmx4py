""" Network utility tests.
"""
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
