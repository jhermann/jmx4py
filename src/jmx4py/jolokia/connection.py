""" JMX Connections. 

    @author: jhe
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

import urllib2

from jmx4py.util import network, json


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
        """ Create a connection from the given URL using the scheme registry.
        """
        try:
            # Support the common socket pair for HTTP connections to the default context
            host, port = url
            
            try:
                port = int(port)
            except (TypeError, ValueError), exc:
                raise urllib2.URLError("Bad port in (host, port) pair %r (%s)" % (url, exc)) 
            
            return JmxHttpConnection("http://%s:%d/jolokia/" % (host, port)) 
        except (TypeError, ValueError): 
            url_scheme = url.split(':', 1)[0].lower()
            if url_scheme not in cls.registry:
                raise urllib2.URLError("Unsupported URl scheme '%s' in '%s'" % (url_scheme, url)) 
                
            return cls.registry[url_scheme](url)


    def __init__(self, url):
        """ Create a proxy connection.
        """
        self.url = url
        self.calls = 0
        self.errors = 0


    def open(self):
        """ Open the connection.
        """
        raise NotImplementedError()


    def close(self):
        """ Close the connection and release associated resources.
        """
        raise NotImplementedError()


    def _do_send(self, data):
        """ Template method performing the connection-specific data transfer.
        """
        raise NotImplementedError()


    def send(self, data):
        """ Perform a single request and return the deserialized response.
        """
        self.calls += 1
        try:
            # TODO: Add latency statistics?
            resp = self._do_send(data)
        except:
            self.errors += 1
            raise
        else:
            if resp.get("status") != 200:
                self.errors += 1
            return resp
            

class JmxHttpConnection(JmxConnection):
    """ JMX Proxy Connection via HTTP.
    """

    def __init__(self, url):
        """ Create a proxy connection.
        """
        super(JmxHttpConnection, self).__init__(url)
        self.url = self.url.rstrip('/') + '/'
        self._open = False


    def open(self):
        """ Open the connection.
        """
        # Currently, we have no connection pooling, so this is basically a NOP
        self._open = True
        return self


    def close(self):
        """ Close the connection and release associated resources.
        """
        self._open = False


    def _do_send(self, data):
        """ Perform a single request and return the deserialized response.
        """ 
        headers = {
            "User-Agent": "jmx4py 0.1", # TODO: add automatic version detection
        }
        req_body = json.dumps(data) # TODO: using data automatically select POST as method 
        req = urllib2.Request(self.url, data=req_body, headers=headers, unverifiable=True)  

        handle = network.urlopen(req) # TODO: , username, password)
        try:
# TODO: wire debugging
#            if debug:
#                log.trace("Reponse headers for %r:\n    %s" % (
#                    url, "\n    ".join(i.strip() for i in handle.info().headers)
#                ))
            result = json.loads(handle.read())
            return result
        finally:
            handle.close()        
