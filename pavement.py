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
import time
import tempfile
from contextlib import closing

from setuptools import find_packages

from paver.easy import *
from paver.setuputils import setup


#
# Project Setup
#
name, version = re.match(r"(\S+) \(([.\d]+)\)", open("debian/changelog").readline()).groups()

# You can override this with a local proxy URL, if available
JOLOKIA_REPO_URL = os.environ.get("JOLOKIA_REPO_URL", "http://labs.consol.de/maven/repository")
jolokia_version = "1.0.0"

project = dict(
    name = name,
    version = version,
    package_dir = {"": "src"},
    packages = find_packages("src", exclude = ["tests"]),
    include_package_data = True,
    zip_safe = True,
    data_files = [
        ("EGG-INFO", [
            "README", "LICENSE", "debian/changelog",
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

options(
    setup = project,
    sphinx = Bunch(
        builddir = "../build",
    ),
)
setup(**project)


#
# Helpers
#
def fail(msg):
    "Print error message and exit"
    error("BUILD ERROR: " + msg)
    sys.exit(1)


def copy_url(url, dest):
    "Helper to copy an URL"
    import urllib2, shutil

    info("GET %s => %s" % (url, dest))
    with closing(urllib2.urlopen(url)) as url_handle:
        with closing(open(dest, "wb")) as dest_handle:
            shutil.copyfileobj(url_handle, dest_handle)


def pylint(opts=""):
    "Call pylint"
    sh("./bin/pylint %s --rcfile pylint.rc --import-graph=%s %s" % (
            opts, path("build/imports.png").abspath(), project["name"]),
        ignore_error=True) # TODO: should check for return code ERROR bits and fail on errors


def run_with_jvm(closure, *args, **kw):
    "Run the provided callable with a live JVM running in the background"
    if not sh("which mvn", capture=True, ignore_error=True): 
        fail("Maven build tool not installed / available on your path!")

    with pushd("java/testjvm") as base_dir:
        # Build test app if not there
        jars = path("target").glob("jmx4py-*.jar")
        if not jars:
            sh("mvn package")
            jars = path("target").glob("jmx4py-*.jar")
            if not jars:
                fail("Maven build failed to produce an artifact!")

        # Get agent if not there
        if not path("target/jolokia-jvm-agent.jar").exists():
            copy_url(
                "%s/org/jolokia/jolokia-jvm/%s/jolokia-jvm-%s-agent.jar" % (JOLOKIA_REPO_URL, jolokia_version, jolokia_version),
                "target/jolokia-jvm-agent.jar")

        # Start test JVM in background
        jolokia_props_path = path(base_dir) / "java" / "jolokia.properties"
        jolokia_props = dict((key, val.strip()) for key, val in (
            line.split(':', 1) for line in jolokia_props_path.lines() if ':' in line))
        guard_file = path("/tmp/jmx4py-test-guard-%d" % os.getuid())
        sh("java -javaagent:target/jolokia-jvm-agent.jar=config=%s -jar %s %s &" % (
            jolokia_props_path, jars[0].abspath(), guard_file))
        for _ in range(50):
            if guard_file.exists():
                print "JVM name:", guard_file.text().strip()
                break
            time.sleep(.1)
        else:
            fail("JVM start failed")

        # Now run the given closure
        try:
            with pushd(base_dir):
                closure(*args, **kw)
        except KeyboardInterrupt:
            fail("Aborted by CTRL-C")
        finally:
            # Stop test JVM
            guard_file.remove()
            time.sleep(1)


#
# Tasks
#
@task
def jvmtests():
    "Run integration tests against a live JVM"
    run_with_jvm(sh, "nosetests -a jvm") # run all tests!


@task
def explore():
    "Run interactive interpreter against a live JVM"
    init = path(tempfile.mkstemp(".py", "jmx4py-")[1])
    init.write_lines([
        "from jmx4py import jolokia",
        "jp = jolokia.JmxClient(('localhost', 8089))",
        "print('Use the following object that was created for you to test the API:\\n')",
        "print('jp = %r\\n' % jp)",
    ])
    run_with_jvm(sh, "bpython -i %s" % init)
    init.remove()


@task
def docs():
    "Build documentation"
    call_task("paver.doctools.html")


@task
def lint():
    "Automatic source code check"
    pylint("-rn")


@task
def tests():
    "Execute unit tests"
    # The nosetests task does dirty things to the process environment, spawn a new process
    sh("nosetests")


@task
def integration():
    "Run all tasks adequate for continuous integration"
    call_task("build")
    call_task("jvmtests")
    pylint(">build/lint.log -ry -f parseable")
    call_task("docs")
    call_task("sdist")
    call_task("bdist_egg")

