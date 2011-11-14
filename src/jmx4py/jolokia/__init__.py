""" Jolokia client API for Python.
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

import socket
import urllib2
import httplib

from jmx4py.jolokia.errors import JmxException
from jmx4py.jolokia.client import JmxClient
from jmx4py.jolokia.connection import JmxConnection, JmxHttpConnection

JmxConnection.register("http", JmxHttpConnection)
JmxConnection.register("https", JmxHttpConnection)

ERRORS = (
    socket.error,
    urllib2.URLError,
    httplib.HTTPException,
    JmxException,
)

__all__ = [
    "ERRORS", "JmxException",
    "JmxClient", "JmxConnection", "JmxHttpConnection",
]
