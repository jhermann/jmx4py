""" Jolokia client proxy tests.
"""
import logging
import unittest
import urllib2

from tests import JmxMockedConnection
from jmx4py.jolokia.connection import JmxHttpConnection
from jmx4py.jolokia.client import * #@UnusedWildImport

log = logging.getLogger(__name__)


class JmxClientTest(unittest.TestCase):
    
    def test_client_connection(self):
        proxy = JmxClient("mock:")
        self.failUnless(isinstance(proxy.connection, JmxMockedConnection))


    def test_host_port(self):
        proxy = JmxClient(("localhost", "8080"))
        self.failUnless(isinstance(proxy.connection, JmxHttpConnection))
        self.failUnlessEqual(proxy.connection.url, "http://localhost:8080/jolokia/")


    def test_bad_scheme(self):
        self.failUnlessRaises(urllib2.URLError, JmxClient, "foobar:")


    def test_bad_port(self):
        self.failUnlessRaises(urllib2.URLError, JmxClient, ("localhost", "x"))

