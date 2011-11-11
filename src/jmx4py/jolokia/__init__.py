""" Jolokia client API for Python.
"""
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
