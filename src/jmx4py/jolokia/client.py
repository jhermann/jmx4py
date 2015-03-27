# -*- coding: utf-8 -*-
# pylint: disable=bad-whitespace, too-few-public-methods
""" JMX Client Proxy.

    See http://www.jolokia.org/reference/html/protocol.html for a
    detailed description of the Jolokia protocol and different ways
    to query for information. The client API methods only describe
    the major points, and specifics of the Python interface.
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

import re
import datetime
from contextlib import closing

from jmx4py.util import json, auxiliary
from jmx4py.jolokia.errors import JmxResponseError
from jmx4py.jolokia.connection import JmxConnection

_QUOTE_RE = re.compile(r"([!/])")
_UNQUOTE_RE = re.compile(r"!(.)")


def quote(path):
    """ Escape a path according to Jolokia v6 rules.
    """
    return _QUOTE_RE.sub(r"!\1", path) if path else path



def unquote(path):
    """ Un-escape a path according to Jolokia v6 rules.
    """
    if not path:
        return path
    if path.endswith('!') and (len(path) - len(path.rstrip('!'))) % 2:
        raise ValueError("Invalid trailing escape in %r" % path)
    return _UNQUOTE_RE.sub(r"\1", path)


#class JmxRequest(object):
#    """ JMX Proxy Request.
#    """
#
#    def __init__(self, **kw):
#        """ Populate request from given keyword arguments.
#        """


class JmxResponse(dict):
    """ JMX Proxy Response. Wraps responses into a fancy accessor.
    """

    def __str__(self):
        """ Return fully nested representation of JMX response (JSON dump).
        """
        return json.dumps(self, indent=2)


    def __repr__(self):
        """ Return short representation of JMX response.

            >>> jp.read("java.lang:type=Memory", "HeapMemoryUsage", path="used")
            <JmxResponse type=read status=200 timestamp=2011-11-15T17:44:50 value=4573856>
        """
        return "<%s type=%s status=%d timestamp=%s value=%s>" % (
            self.__class__.__name__, self["request"]["type"], self["status"],
            datetime.datetime.fromtimestamp(self["timestamp"]).isoformat(),
            auxiliary.digest_repr(self["value"]),
        )


    def __getitem__(self, key):
        try:
            return super(JmxResponse, self).__getitem__(key)
        except KeyError:
            if '.' in key:
                namespace = self["value"]
                for part in key.split('.'):
                    namespace = namespace.get(part, None)
                    if not namespace:
                        break
                return namespace
            elif key in self["value"]:
                return self["value"][key]
            raise


    def __getattr__(self, name):
        try:
            # TODO: Check if there's such a wrapper already out there!
            # TODO: Need to handle nested access (response.foo.bar)
            return self[name]
        except KeyError:
            return getattr(super(JmxResponse, self), name)



class JmxClientConfig(object):
    """ JMX Client Proxy Configuration.

        TODO: atually pass these on to the connection!
        user        User name when authentication is used.
                    If not set, no authentication is used. If set, password must be set, too
        password    Password used for authentication. Only used when user is set.

        TODO: more parameters?
        timeout     The timeout in seconds for network operations.
        contentCharset     Defines the charset to be used per default for encoding content body.     ISO-8859-1
        expectContinue     Activates Expect: 100-Continue handshake for the entity enclosing methods.
            The purpose of the Expect: 100-Continue handshake to allow a client that is sending
            a request message with a request body to determine if the origin server is willing
            to accept the request (based on the request headers) before the client sends the
            request body. The use of the Expect: 100-continue handshake can result in noticable
            peformance improvement for entity enclosing requests that require the target server's
            authentication.     true
    """

    def __init__(self, url, **kw):
        """ Store configuration as given in keyword parameters, mixing in default values.
        """
        self.url = url
        self.user = kw.get("user", None)
        self.password = kw.get("password", None)
        self.method = kw.get("method", "POST")
        #self. = kw.get("", None)


class JmxClient(object):
    """ JMX Client Proxy.
    """
    # TODO: Historical values - http://www.jolokia.org/reference/html/protocol.html#history
    # TODO: Support bulk requests - http://www.jolokia.org/reference/html/protocol.html#post-request

    def __init__(self, url, **kw):
        """ Open a proxy connection to a Jolokia agent.
        """
        self.cfg = JmxClientConfig(url, **kw)
        self.connection = JmxConnection.from_url(self.cfg.url)


    def __repr__(self):
        """ Return client proxy identification.
        """
        return "%s(%r)" % (self.__class__.__name__, self.connection.url)


    def _execute(self, **kw):
        """ Execute a request as defined by the given keyword arguments.

            TODO: Do we need this?
            MAX_DEPTH     Maximum traversal depth for serialization of complex objects.
                Use this with a "list" request to restrict the depth of the returned meta data tree.
            MAX_COLLECTION_SIZE     Maximum size of collections returned during serialization.
                If larger, a collection is truncated to this size.
            MAX_OBJECTS     Maximum number of objects returned in the response's value.
            IGNORE_ERRORS     Option for ignoring errors during JMX operations and JSON serialization.
                This works only for certain operations like pattern reads and should be either true or false.
        """
        req = kw # pass on unchanged keyword params, for now

        with closing(self.connection.open()) as handle:
            resp = JmxResponse(handle.send(req))
            if resp.status != 200:
                raise JmxResponseError(resp, req)
            return resp


    def read(self, mbean, attribute=None, path=None, **kw):
        """ A read request gets one or more attributes from one or more
            MBeans within a single request.

            Various call variants can be used to specify one or more
            attributes along with the JMX ObjectName (which can be a pattern). A
            path can be set as property for specifying an inner path, too.

            A read request for multiple attributes on the same MBean is initiated
            by giving a list of attributes to the request. If no attribute is
            provided, then all attributes are fetched. The MBean name can be
            given as a pattern in which case the attributes are read on all
            matching MBeans. If a MBean pattern and multiple attributes are
            requestes, then only the value of attributes which matches both
            are returned, the others are ignored. Paths cannot be used with
            multi value reads, though.
        """
        req = dict(type = "read", mbean = mbean)
        if attribute:
            req["attribute"] = attribute
        if path:
            req["path"] = quote(path)
        if kw:
            req.update(kw)
        resp = self._execute(**req)
        return resp


    def write(self):
        """ TODO: Implement write()
            J4pWriteRequest and J4pWriteResponse

                A J4pWriteRequest is used to set the value of an MBean
            attribute. Beside the mandatory object and attribute name the
            value must be give in the constructor as well. Optionally a path
            can be provided, too. Only certain types for the given value can
            be serialized properly for calling the Jolokia agent as described
            in Section 6.4.2, "Request parameter serialization".

                The old value is returned as J4pWriteResponse's value.
            J4pExecRequest and J4pExecResponse

        """
        resp = self._execute(type = "write")
        return resp


    def invoke(self):
        """ TODO: Implement invoke()
                J4pExecRequests are used for executing operation on MBeans.
            The constructor takes as mandatory arguments the MBean's object
            name, the operation name and any arguments required by the
            operation. Only certain types for the given arguments can be
            serialized properly for calling the Jolokia agent as described in
            Section 6.4.2, "Request parameter serialization".

                The returned J4pExecResponse contains the return value of the
            operation called.
            J4pSearchRequest and J4pSearchResponse

        """
        resp = self._execute(type = "invoke")
        return resp


    def search(self):
        """ TODO: Implement search()
                A J4pSearchRequest contains a valid single MBean object name
            pattern which is used for searching MBeans.

                The J4pSearchResponse holds a list of found object names.
            J4pListRequest and J4pListResponse

                For obtaining meta data on MBeans a J4pListRequest should be
            used. It can be used with a inner path to obtain only a subtree
            of the response, otherwise the whole tree as described in Section
            6.2.5.3, "List response" is returned. With the query parameter
            maxDepth can be used to restrict the depth of returned tree.

                The single value of a J4pListResponse is a tree (or subtree)
            as a JSON object, which has the format described in Section
            6.2.5.3, "List response".
            J4pVersionRequest

        """
        resp = self._execute(type = "search")
        return resp


    def version(self):
        """ Request the Jolokia agent's version information.
            See JmxResponse for ways to access the result.

            >>> import jmx4py.jolokia
            >>> jp = jmx4py.jolokia.JmxClient(("localhost", 8089))
            >>> jp
            JmxClient('http://localhost:8089/jolokia/')
            >>> jp.version().protocol_info[:1]
            (6,)
            >>> jp.version().agent_info[:2]
            (1, 0)
        """
        resp = self._execute(type = "version")
        resp["value"]["protocol_info"] = tuple(int(i) for i in resp.protocol.split('.'))
        resp["value"]["agent_info"] = tuple(int(i) for i in resp.agent.split('.'))
        return resp
