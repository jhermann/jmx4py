""" JMX Exceptions. 

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

class JmxException(Exception):
    """ JMX exception base class.
    """


class JmxResponseError(JmxException):
    """ Indicates request results containing an error status.
    """

    def __init__(self, response, request=None):
        """ Extract major fields from an error response and map it to
            common Python conventions.
        """
        super(JmxResponseError, self).__init__(response, request)

        # "code" and "reason" are more common in Python (httplib)
        self.code = self.status = response.get("status", -1)
        self.reason = self.error = response.get("error", "<unknown JMX error>")
        self.request = request or {}
        self.response = response


    def __str__(self):
        """ Generate concise description of an error.
        """
        return "status %d for %s operation: %s" % (
            self.code, self.request.get("type", "UNKNOWN"), self.reason,
        )


    def __repr__(self):
        """ Generate concise representation of an error.
        """
        return "<%s %s>" % (self.__class__.__name__, self)
