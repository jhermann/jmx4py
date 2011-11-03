""" JMX Client Proxy. 

    @author: jhe
"""
from jmx4py.jolokia.connection import JmxConnection


class JmxClient(object):
    """ JMX Client Proxy.
    """

    def __init__(self, server_url):
        """ Open a proxy connection to a Jolokia agent.
        """
        self.connection = JmxConnection.from_url(server_url)

        