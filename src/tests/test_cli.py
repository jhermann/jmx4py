
# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import, missing-docstring
# pylint: disable=redefined-outer-name, no-self-use, bad-continuation
""" Test '__main__' CLI stub.

    See http://click.pocoo.org/3/testing/
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

import sys

import sh
import pytest
from click.testing import CliRunner

from markers import *
from jmx4py import __version__ as version
from jmx4py import __main__ as main


UsageError = sh.ErrorReturnCode_2  # pylint: disable=no-member


@pytest.fixture
def cmd():
    """Command fixture."""
    return sh.Command(main.__app_name__)


@cli
@integration
def test_cli_help(cmd):
    result = cmd('--help')
    lines = result.stdout.decode('ascii').splitlines()

    assert main.__app_name__ in lines[0].split(), "Command name is reported"


@cli
@integration
def test_cli_version(cmd):
    result = cmd('--version')
    stdout = result.stdout.decode('ascii')
    reported_version = stdout.split()[1]
    py_version = sys.version.split()[0]

    assert version in stdout, "Version string contains version"
    assert reported_version[:len(version)] == version, "Version is 2nd field"
    assert py_version in stdout, "Python version is reported"


@cli
@integration
def test_cli_invalid_option(cmd):
    with pytest.raises(UsageError):
        cmd('--this-is-certainly-not-a-supported-option')


@cli
@integration
def test_cli_invalid_sub_command(cmd):
    with pytest.raises(UsageError):
        cmd.sub_command_that_does_not_exist()


@cli
def test_cmd_missing():
    runner = CliRunner()
    result = runner.invoke(main.cli)

    assert result.exit_code == 0


@cli
def test_cmd_help():
    runner = CliRunner()
    result = runner.invoke(main.help_command)
    word1 = result.output.split()[0]

    assert result.exit_code == 0
    assert word1 == 'Helpful', "Helpful message is printed"

