""" Generic helper functions. 

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

def digest_repr(obj):
    """ Return a short digest of a possibly deeply nested (JSON) object. 
    """ 
    if isinstance(obj, (tuple, list, set, dict)):
        def nesting(collection):
            "Helper"
            if isinstance(collection, dict):
                collection = collection.values()
            if isinstance(collection, (tuple, list, set)):
                return 1 + max(nesting(i) for i in collection)
            else:
                return 1

        depth = nesting(obj)
        contents = list(obj)
        if len(contents) > 10:
            contents[3:-2] = "..." 
        return "<%s of maxdepth %d and len %d holding %s>" % (
            type(obj).__name__, depth, len(obj), ', '.join(repr(i) for i in contents))
    else:
        return repr(obj) # Normal repr() for scalar or other non-collection objects
