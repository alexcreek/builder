import os
from subprocess import check_output
import pytest
from builder.project import Project

url = 'git@github.com:alexcreek/builder.git'
commit = '5eeac3d0ce75609214d091a6fa4229c991be5065'
branch = 'refs/heads/test_fixture'

# create a new instance of Project for each test
@pytest.fixture
def project():
    p = Project(url, commit, branch)
    return p

def test_checkout(project):
    project.checkout()
    o = check_output(["git", "-C", project.path, "rev-parse", "HEAD" ])
    assert os.path.isdir(project.path)
    # checkout_output returns a byte string
    assert o.decode('utf-8').strip() == commit

def test_parse_manifest(project):
    # There's a Builderfile in the tests directory.
    project.path = 'tests'
    project.parse_manifest()

    with pytest.raises(SystemExit) as e:
    # There's not a Builderfile in tmp
        project.path = 'tmp'
        project.parse_manifest()
    assert e.type == SystemExit

def test_build(project):
    project.path = 'tests'
    project.parse_manifest()
    project.build()

def test_cleanup(project):
    project.checkout()
    project.cleanup()
    assert not os.path.isdir(project.path)
