""" Jolokia client API for Python.
"""
import socket
import urllib2
import httplib

from jmx4py.jolokia.errors import JmxException
from jmx4py.jolokia.client import JmxClient


ERRORS = (
    socket.error,
    urllib2.URLError,
    httplib.HTTPException,
    JmxException,
)

__all__ = [
    "ERRORS",
    "JmxException",
    "JmxClient",
]
