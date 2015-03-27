# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, wildcard-import, unused-wildcard-import
# pylint: disable=too-few-public-methods, bad-continuation
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
from __future__ import absolute_import, unicode_literals, print_function

import logging
import unittest
import urllib2

from conftest import JmxMockedConnection, JvmTestCase
from jmx4py.jolokia.connection import JmxHttpConnection
from jmx4py.jolokia.client import * #@UnusedWildImport

log = logging.getLogger(__name__)


class JmxEscapingTest(unittest.TestCase):

    # Unescaped and escaped test data
    DATA = (
        (None, None),
        ("", ""),
        ("a", "a"),
        ("!", "!!"),
        ("a/b", "a!/b"),
        ("a/b/c", "a!/b!/c"),
        ("a!b/c", "a!!b!/c"),
    )

    def test_quote(self):
        for text, quoted in self.DATA:
            self.assertEqual(quote(text), quoted)


    def test_unquote(self):
        for text, quoted in self.DATA:
            self.assertEqual(text, unquote(quoted))


    def test_unquote_extra(self):
        self.assertEqual("ab!/z", unquote("!a!b!!!/!z"))


    def test_unquote_trail(self):
        self.failUnlessRaises(ValueError, unquote, "!")
        self.failUnlessRaises(ValueError, unquote, "!!!")


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


class JmxClientBasicsTest(JvmTestCase):

    def test_repr(self):
        self.failUnless("localhost" in repr(self.proxy))


    def test_bad_type(self):
        self.failUnlessRaises(JmxResponseError, self.proxy._execute, type="foo bar baz")

        self.failUnlessEqual(self.proxy.connection.calls, 1)
        self.failUnlessEqual(self.proxy.connection.errors, 1)


class JmxClientReadTest(JvmTestCase):

    def test_read(self):
        resp = self.proxy.read("java.lang:type=Memory")
        self.failUnless(all(i in resp.value for i in ["HeapMemoryUsage", "NonHeapMemoryUsage"]))


    def test_read_with_path(self):
        resp = self.proxy.read("java.lang:type=Memory", "HeapMemoryUsage", "used")
        self.failUnless(isinstance(resp.value, int))


    def test_multi_read(self):
        resp = self.proxy.read("java.lang:type=Memory", ["HeapMemoryUsage", "NonHeapMemoryUsage"])
        self.failUnlessEqual(set(resp.value.keys()), set(["HeapMemoryUsage", "NonHeapMemoryUsage"]))


    def test_multi_read_with_path(self):
        self.failUnlessRaises(JmxResponseError, self.proxy.read,
            "java.lang:type=Memory", ["HeapMemoryUsage", "NonHeapMemoryUsage"], "used")


class JmxClientWriteTest(JvmTestCase):

    def test_write(self):
        pass
        #TODO: resp = self.proxy.write("java.lang:type=...", ...)


class JmxClientInvokeTest(JvmTestCase):

    def test_invoke(self):
        pass # TODO: write test


class JmxClientSearchTest(JvmTestCase):

    def test_search(self):
        pass # TODO: write test


class JmxClientVersionTest(JvmTestCase):

    def test_version(self):
        version = self.proxy.version()

        self.failUnlessEqual(self.proxy.connection.calls, 1)
        self.failUnlessEqual(self.proxy.connection.errors, 0)

        self.failUnlessEqual(version["status"], 200)
        self.failUnless(isinstance(version["timestamp"], int))
        self.failUnlessEqual(version["request"]["type"], "version")
        self.failUnless(version.protocol.startswith("6."))
