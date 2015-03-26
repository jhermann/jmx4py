# TODO: Copy the remainder to tasks.py
""" jmx4py - A Python Client for the Jolokia JMX Agent.
"""

# You can override this with a local proxy URL, if available
JOLOKIA_REPO_URL = os.environ.get("JOLOKIA_REPO_URL", "http://labs.consol.de/maven/repository")
jolokia_version = "1.0.0"

project = dict(
    data_files = [
        ("EGG-INFO", [
            "README", "LICENSE", "debian/changelog",
        ]),
    ],
)

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


def stop_all_jvms():
    "Stop all running test JVMs."
    running_agents = [i.split(None, 1)
        for i in sh("jps -m", capture=True, ignore_error=True).splitlines()
        if "jmx4py-testjvm" in i
    ]
    for pid, cmd in running_agents:
        pid = int(pid, 10)
        info("Stopping '%s' (PID=%d)" % (cmd, pid))
        os.kill(pid, signal.SIGTERM)
        for _ in range(25):
            time.sleep(0.1)
            try:
                os.kill(pid, signal.SIGTERM)
            except EnvironmentError:
                break
        else:
            info("WARNING: JVM '%s' (PID=%d) could not be stopped" % (cmd, pid))


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
        stop_all_jvms()
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
            time.sleep(.25)
            stop_all_jvms()


#
# Tasks
#
@task
@needs(["clean"])
def clean_dist():
    "Clean up build and dist files."
    path("dist").rmtree()


@task
@needs(["clean_dist"])
def clean_all():
    "Clean up everything."
    # clean up local eggs (setup requirements)
    for name in path(".").dirs("*.egg"):
        path(name).rmtree()
    for name in path(".").files("*.egg"):
        path(name).remove()

    # get rid of virtualenv environment
    bindir = path("bin")
    if not bindir.islink():
        for exe in bindir.files():
            path(exe).remove()
    for dirname in ("lib", "include", "Scripts"):
        path(dirname).rmtree()


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
@needs('generate_setup', 'minilib', 'distutils.command.sdist')
def sdist():
    "Package a source distribution"


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
