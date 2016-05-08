# jmx4py

![Logo](https://raw.github.com/jhermann/jmx4py/master/docs/_static/jmx4py-logo-64.png)

A Python Client for the Jolokia JMX Agent

 [![Travis CI](https://api.travis-ci.org/jhermann/jmx4py.svg)](https://travis-ci.org/jhermann/jmx4py)
 [![GitHub Issues](https://img.shields.io/github/issues/jhermann/jmx4py.svg)](https://github.com/jhermann/jmx4py/issues)
 [![License](https://img.shields.io/pypi/l/jmx4py.svg)](https://github.com/jhermann/jmx4py/blob/master/LICENSE)
 [![Development Status](https://pypip.in/status/jmx4py/badge.svg)](https://pypi.python.org/pypi/jmx4py/)
 [![Latest Version](https://img.shields.io/pypi/v/jmx4py.svg)](https://pypi.python.org/pypi/jmx4py/)
 [![Download format](https://pypip.in/format/jmx4py/badge.svg)](https://pypi.python.org/pypi/jmx4py/)
 [![Downloads](https://img.shields.io/pypi/dw/jmx4py.svg)](https://pypi.python.org/pypi/jmx4py/)


## Overview

Jolokia is a JMX-HTTP bridge giving an alternative to JSR-160 connectors.
It is an agent based approach with support for many platforms. In addition
to basic JMX operations it enhances JMX remoting with unique features like
bulk requests or fine grained security policies.

jmx4py offers a client API similar to the existing Jolokia clients for Perl
(jmx4perl), Java and Javascript. Additionally, it'll build upon the basic
API and offer further features related to monitoring and controlling JVMs
via JMX using Python.


## Setup

To create a working directory for this project,
follow these steps on a POSIX system:

```sh
git clone "https://github.com/jhermann/jmx4py.git"
cd "jmx4py"
. .env --yes --develop
invoke build --docs test check
```

The ``.env`` script creates a virtualenv and
installs the necessary tools into it.
See the script for details.

Now you can explore the API by simply issuing the following command:

    invoke explore

For that to succeed, you must also have a working Java + Maven environment,
since a small test application is built and then started in the background,
so you can work against a live JVM.

See [CONTRIBUTING](https://github.com/jhermann/jmx4py/blob/master/CONTRIBUTING.md) for more.


## Installation

**TODO**: pip install / dh-virtualenv


## Usage

jmx4py offers the following command line tools... **TODO**

For using jmx4py from Python, consult the API documentation available at **TODO**


## Known Limitations & Issues

* The API is subject to change for 0.x, until enough practical experience is gained.
* Only Jolokia 1.0 and up (Protocol v6) is supported.
* GET requests aren't supported.
* Bulk requests aren't supported.
* Python 2.7 is used for development, and 2.7 and 3.4 are tested in continuous integration.


## References

**Project**

* [jmx4py @ PyPI](http://pypi.python.org/pypi/jmx4py/)
* [jmx4py @ Open HUB](https://www.openhub.net/p/jmx4py)
* [Jolokia](http://www.jolokia.org/)

**Tools**

* [Cookiecutter](http://cookiecutter.readthedocs.io/en/latest/)
* [PyInvoke](http://www.pyinvoke.org/)
* [pytest](http://pytest.org/latest/contents.html)
* [tox](https://tox.readthedocs.io/en/latest/)
* [Pylint](http://docs.pylint.org/)
* [twine](https://github.com/pypa/twine#twine)
* [bpython](http://docs.bpython-interpreter.org/)
* [yolk3k](https://github.com/myint/yolk#yolk)

**Packages**

* [Rituals](https://jhermann.github.io/rituals)
* [Click](http://click.pocoo.org/)


## Acknowledgements

…
