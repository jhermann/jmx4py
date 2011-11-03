""" Unit tests.
"""
from jmx4py.jolokia.connection import JmxConnection


class JmxMockedConnection(JmxConnection):
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

JmxConnection.register("mock", JmxMockedConnection)
