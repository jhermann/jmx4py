""" Jolokia client proxy tests.
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

from tests import JmxMockedConnection, JvmTestCase
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


class JmxClientJvmTest(JvmTestCase):

    def test_repr(self):
        self.failUnless("localhost" in repr(self.proxy))
        
    
    def test_version(self):
        version = self.proxy.version()

        self.failUnlessEqual(version["status"], 200)
        self.failUnless(isinstance(version["timestamp"], int))
        self.failUnlessEqual(version["request"]["type"], "version")
        self.failUnless(version.protocol.startswith("6."))
