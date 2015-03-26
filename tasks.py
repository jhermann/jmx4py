# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import, bad-continuation
""" Project automation for Invoke.
"""
from __future__ import absolute_import, unicode_literals

import os
import shutil
import tempfile

from invoke import run, task
from rituals.invoke_tasks import * # pylint: disable=redefined-builtin


@task(name='fresh-cookies',
    help={
        'mold': "git URL or directory to use for the refresh",
    },
)
def fresh_cookies(mold=''):
    """Refresh the project from the original cookiecutter template."""
    mold = mold or "https://github.com/Springerle/py-generic-project.git"  # TODO: URL from config
    tmpdir = os.path.join(tempfile.gettempdir(), "moar-jmx4py")

    if os.path.isdir('.git'):
        # TODO: Ensure there are no local unstashed changes
        pass

    # Make a copy of the new mold version
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    if os.path.exists(mold):
        shutil.copytree(mold, tmpdir, ignore=shutil.ignore_patterns(
            ".git", ".svn", "*~",
        ))
    else:
        run("git clone {} {}".format(mold, tmpdir), echo=True)

    # Copy recorded "cookiecutter.json" into mold
    shutil.copy2("project.d/cookiecutter.json", tmpdir)

    with pushd('..'):
        run("cookiecutter --no-input {}".format(tmpdir), echo=True)
    if os.path.exists('.git'):
        run("git status", echo=True)


@task(help={
    'verbose': "Make 'tox' more talkative",
    'env-list': "Override list of environments to use (e.g. 'py27,py34')",
    'opts': "Extra flags for tox",
})
def tox(verbose=False, env_list='', opts=''):
    """Perform multi-environment tests."""
    snakepits = ['/opt/pyenv/bin'] # TODO: config value
    cmd = []

    snakepits = [i for i in snakepits if os.path.isdir(i)]
    if snakepits:
        cmd += ['PATH="{}:$PATH"'.format(os.pathsep.join(snakepits),)]

    cmd += ['tox']
    if verbose:
        cmd += ['-v']
    if env_list:
        cmd += ['-e', env_list]
    cmd += opts
    cmd += ['2>&1']
    run(' '.join(cmd), echo=True)


@task(help={
    'pty': "Whether to run commands under a pseudo-tty",
}) # pylint: disable=invalid-name
def ci(pty=True):
    """Perform continuous integration tasks."""
    opts = ['']

    # 'tox' makes no sense in Travis
    if os.environ.get('TRAVIS', '').lower() == 'true':
        opts += ['test']
    else:
        opts += ['tox']

    run("invoke clean --all build --docs check --reports{} 2>&1".format(' '.join(opts)), echo=True, pty=pty)
