import os
from subprocess import check_output
import pytest
from builder.project import Project

url = 'git@github.com:alexcreek/builder.git'
commit = '6a9d4aeee29927ca4baed7d67f8ba4eb548bf10b'
branch = 'refs/heads/test_fixture'
status_url = 'https://api.github.com/repos/alexcreek/builder/statuses/{sha}'

# create a new instance of Project for each test
@pytest.fixture
def project():
    p = Project(url, commit, branch, status_url)
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
