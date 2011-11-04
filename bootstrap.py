#! /usr/bin/env python
""" Bootstrap script for setting up a development environment.

    - Add "full" as an argument to install optional tools.
    - Add "local" as an argument to force the creation of a virtual
      environment in the working directory.
    - Add "clean" as an argument to start fresh (remove "bin", "lib",
      and "include" before boot-strapping).

    This either uses an already activated Python virtualenv (e.g. a
    pydev/Eclipse one), or creates a virtualenv in the working directory,
    and then installs the basic tooling to get you started. The script
    works for any project that is built using Paver, and it has no extra
    requirements on the host beyond a basic Python installation.
"""
import os
import sys
import glob
import urllib2
import shutil
import subprocess

VENV_ARGS = ["--no-site-packages"]
VENV_PY = 'https://github.com/pypa/virtualenv/raw/master/virtualenv.py'
INSTALL_ARGS = [
    "-i", "http://pypi.python.org/pypi",
    "-U",
]
TOOLS = [ # what you need pretty much always
    "distribute>=0.6",
    "yolk",
    "Paver>=1.0",
    # Version hell is as follows:
    # - nosexcover only works with coverage==3.4, but that isn't downloadable any more, thus a patch is needed
    # - NoseXUnit 0.3.3 has a fixed dependency to coverage==2.85, which sucks, especially since it (sometimes) works with 3.4!
    "coverage>=3.4",
    "nose>=0.11.1",
    ##"?NoseXUnit", is broken
    "nosexcover",
]
EXTRA_TOOLS = [ # only needed in integration builds and for releasing
    "Sphinx",
    "pylint",
    "bpython",
]


def _get_real_python():
    "Get path to the machine's python executable."
    is_venv = False
    
    # Get executable path
    python_exe = sys.executable
    python_version = '.'.join(str(i) for i in sys.version_info[:2])
    if os.path.exists(python_exe + python_version):
        python_exe += python_version

    # Try to get executable from virtualenv metadata
    lib_dirs = glob.glob(os.path.join(
        os.path.dirname(os.path.dirname(python_exe)), "lib/python?*"
    ))
    if lib_dirs:
        # Assume we always want the highest Python version in a virtualenv
        orig_prefix = os.path.join(sorted(lib_dirs)[-1], "orig-prefix.txt")

        # If there's no "orig-prefix.txt", then we already have the right python_exe
        if os.path.exists(orig_prefix):
            with open(orig_prefix, "r") as handle:
                orig_prefix = handle.readline().strip()
            python_exe = os.path.join(orig_prefix, "bin", os.path.basename(python_exe))
            if not os.path.exists(python_exe):
                python_exe = os.path.join(orig_prefix, "bin", "python")
            is_venv = True

    python_exe = os.path.realpath(python_exe)
    return is_venv, python_exe


def _install_dependency(dependency, venv_dir):
    "Install helper, if dependency starts with '?' it's optional (i.e. installation errors are ignored)"
    print
    print "~~~ " + (dependency + ' ').ljust(74, '~')

    installer = os.path.join(venv_dir, "Scripts", "easy_install.exe")
    if not os.path.exists(installer):
        installer = os.path.join(venv_dir, "bin", "easy_install")

    call = subprocess.check_call
    if dependency.startswith('?'):
        dependency = dependency[1:]
        call = subprocess.call
    
    call([installer] + INSTALL_ARGS + [dependency])


def run():
    "Bootstrapper"
    if len(sys.argv) > 1 and sys.argv[1] in ("-?", "-h", "--help"):
        sys.stderr.write(__doc__.strip() + '\n')
        sys.exit(1)

    if "clean" in sys.argv:
        for dirname in ("bin", "build", "include", "lib"):
            os.path.isdir(dirname) and shutil.rmtree(dirname)

    venv_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(venv_dir)
    is_venv, real_python = _get_real_python()
    if is_venv and "local" not in sys.argv:
        print "Using existing Python virtualenv in '%s'" % (sys.prefix,)
        if os.name == 'posix' and not os.path.isdir("bin"):
            # Provide easy access to tools
            os.symlink(os.path.dirname(sys.executable), "bin")
        venv_dir = sys.prefix
    elif not os.path.exists("bin/python"):
        print "Creating new Python virtualenv in '%s'" % (venv_dir,)
        with open("venv.py", 'w') as handle:
            handle.write(urllib2.urlopen(VENV_PY).read())
        subprocess.check_call([real_python, "venv.py"] + VENV_ARGS + [venv_dir])
        os.remove("venv.py")

    for tool in TOOLS:
        _install_dependency(tool, venv_dir)

    if "full" in sys.argv:
        for tool in EXTRA_TOOLS:
            _install_dependency(tool, venv_dir)

    # Fix broken nose plugins...
    # If you want full unittest support on Windows, use cygwin/bash, or apply the patch manually
    subprocess.call(
        """sed -ie 's/if self.coverErase/if getattr(self, "coverErase", False)/'"""
        """ $(find lib/ -path '*/nose/plugins/cover.py')""", shell=True
    )
    #sed -ie 's/coverage == 2.85/coverage >= 2.85/' \
    #$(find lib/ -path '*/site-packages/NoseXUnit*/EGG-INFO/requires.txt')

    subprocess.call("./bin/paver develop -U", shell=True)


if __name__ == "__main__":
    run()

