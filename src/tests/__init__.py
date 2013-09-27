""" Unit tests.
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

import unittest
from nose.plugins.attrib import attr

from jmx4py.jolokia import client, connection


class JmxMockedConnection(connection.JmxConnection):
    """ JMX Proxy Connection Mock.
    """

    def __init__(self, url):
        """ Create a proxy connection.
        """
        super(JmxMockedConnection, self).__init__(url)


    def open(self):
        """ Open the connection.
        """


    def close(self):
        """ Close the connection and release associated resources.
        """


    def _do_send(self, data):
        """ Perform a single request and return the deserialized response.
        """

connection.JmxConnection.register("mock", JmxMockedConnection)


@attr("jvm")
class JvmTestCase(unittest.TestCase):
    """ Test base class that provides an already prepared client.
    """

    def setUp(self):
        self.proxy = client.JmxClient(("localhost", 8089))
