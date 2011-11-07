""" Unit tests.
"""
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

connection.JmxConnection.register("mock", JmxMockedConnection)


@attr("jvm")
class JvmTestCase(unittest.TestCase):
    """ Test base class that provides an already prepared client.
    """ 
    
    def setUp(self):
        self.proxy = client.JmxClient(("localhost", 8089))  
