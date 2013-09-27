jmx4py - A Python Client for the Jolokia JMX Agent
==================================================

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

To create a working directory, follow these steps on a POSIX system:

    git clone git://github.com/jhermann/jmx4py.git
    cd jmx4py
    ./bootstrap.py clean full local
    . ./bin/activate

Note that an already activated Python virtualenv is used for the project,
otherwise a new one is created locally. In either case necessary tools are
then installed into the chosen virtualenv. See the bootstrap script for
details.

A similar procedure should work on Windows, but is not yet tested (reports welcome):

    git clone git://github.com/jhermann/jmx4py.git
    cd jmx4py
    python bootstrap.py clean full local

Then you can explore the API by simply issuing the following command:

    paver explore

For that to suceed, you must also have a working Java + Maven environment,
since a small test application is built and then started in the background,
so you can work against a live JVM.


## Installation

TODO: setup.py install / pip install / virtualenv install


## Usage

jmx4py offers the following command line tools... TODO

For using jmx4py from Python, consult the API documentation available at TODO


## Known Limitations and Issues

  - The API is subject to change for 0.x, until enough practical experience is gained
  - Only Jolokia 1.0 and up (Protocol v6) is supported
  - GET requests aren't supported
  - Bulk requests aren't supported
  - Python 2.6 is used for development and continuous integration, Python 2.7 should work, Python 2.5 MIGHT work


## References
  - [Jolokia](http://www.jolokia.org/)
  - [jmx4py @ PyPI](http://pypi.python.org/pypi/jmx4py/)
  - [jmx4py @ freshmeat](http://freshmeat.net/projects/jmx4py)
  - [jmx4py @ ohloh](https://www.ohloh.net/p/jmx4py)
  - [Paver](http://paver.github.com/paver/)
