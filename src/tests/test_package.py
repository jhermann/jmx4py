# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
""" Test the package metadata.
"""
# Copyright ©  2011 Jürgen Hermann <jh@web.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function

from jmx4py import __version__ as version


def test_semver():
    """Test a proper semantic version is used."""
    # TODO Test rules according to PEP440 – Version Identification and Dependency Specification
    assert len(version.split('.')) == 3, "Semantic version M.m.µ OK"
    assert all(i.isdigit for i in version.split('.')), "Semantic version parts are numeric"
