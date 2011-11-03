""" JMX Connections. 

    @author: jhe
"""
import urllib2


class JmxConnection(object):
    """ JMX Proxy Connection base class.
    """

    # Registry of URL schemes for different connection types
    registry = {}


    @classmethod
    def register(cls, url_scheme, factory):
        """ Register a connection factory for the given URL scheme.
        """
        cls.registry[url_scheme.lower()] = factory


    @classmethod
    def from_url(cls, url):
        try:
            # Support the common socket pair for HTTP connections to the default context
            host, port = url
            
            try:
                port = int(port)
            except (TypeError, ValueError), exc:
                raise urllib2.URLError("Bad port in (host, port) pair %r (%s)" % (url, exc)) 
            
            return JmxHttpConnection("http://%s:%d/jolokia" % (host, port)) 
        except (TypeError, ValueError): 
            url_scheme = url.split(':', 1)[0].lower()
            if url_scheme not in cls.registry:
                raise urllib2.URLError("Unsupported URl scheme '%s' in '%s'" % (url_scheme, url)) 
                
            return cls.registry[url_scheme](url)


    def __init__(self, url):
        """ Create a proxy connection.
        """
        self.url = url


    def open(self):
        """ Open the connection.
        """
        raise NotImplementedError()


    def close(self):
        """ Close the connection and release associated resources.
        """
        raise NotImplementedError()


class JmxHttpConnection(JmxConnection):
    """ JMX Proxy Connection via HTTP.
    """

    def __init__(self, url):
        """ Create a proxy connection.
        """
        url = url.rstrip('/') + '/'
        super(JmxHttpConnection, self).__init__(url)


    def open(self):
        """ Open the connection.
        """
        raise NotImplementedError()


    def close(self):
        """ Close the connection and release associated resources.
        """
        raise NotImplementedError()
