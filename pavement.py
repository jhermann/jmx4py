""" jmx4py - A Python Client for the Jolokia JMX Agent.

    Jolokia is a JMX-HTTP bridge giving an alternative to JSR-160 connectors. 
    It is an agent based approach with support for many platforms. In addition 
    to basic JMX operations it enhances JMX remoting with unique features like 
    bulk requests or fine grained security policies. 

    jmx4py offers a client API similar to the existing Jolokia clients for Perl 
    (jmx4perl), Java and Javascript. Additionally, it'll build upon the basic
    API and offer further features related to monitoring and controlling JVMs
    via JMX using Python.
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

import os
import re
import sys

from setuptools import find_packages

from paver.easy import *
from paver.setuputils import setup


#
# Project Setup
#
name, version = re.match(r"(\S+) \(([.\d]+)\)", open("debian/changelog").readline()).groups()

project = dict(
    name = name,
    version = version,
    package_dir = {"": "src"},
    packages = find_packages("src", exclude = ["tests"]),
    include_package_data = True,
    zip_safe = True,
    data_files = [
        ("EGG-INFO", [
            "README", "TODO", "LICENSE", "debian/changelog",
        ]),
    ],

    # Dependencies
    install_requires = [
    ],
    setup_requires = [
    ],

    # Unit Tests
    test_suite = "nose.collector",

    # PyPI
    author = "Juergen Hermann",
    author_email = "jh@web.de",
    description = __doc__.split('.', 1)[0].strip(),
    long_description = __doc__.split('.', 1)[1].strip(),
    license = "Apache License, Version 2.0",
    url = "https://github.com/jhermann/jmx4py",
    keywords = "python java jmx jolokia http rest json",
    classifiers = [
        # See http://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        #"Topic :: System :: Clustering",
        #"Topic :: System :: Distributed Computing",
        #"Topic :: Utilities",
    ],
)


#
# Helpers
#
def fail(msg):
    "Print error message and exit."
    error("BUILD ERROR: " + msg)
    sys.exit(1)


#
# Tasks
#
@task
def functest():
    "Integration tests against a live JVM"
    if not sh("which mvn", capture=True, ignore_error=True): 
        fail("Maven build tool not installed / available on your path!")

    with pushd("java/testjvm") as base_dir:
        jars = path("target").glob("jmx4py-*.jar")
        if not jars:
            sh("mvn package")
            jars = path("target").glob("jmx4py-*.jar")
            if not jars:
                fail("Maven build failed to produce an artifact!")

        sh("java -jar %s" % jars[0].abspath())


#
# Main
#
print sys.argv
#setup(**project)

