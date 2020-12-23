import os
from subprocess import check_output
import pytest
import requests

class MockResponse:
    def __init__(self):
        self.status_code = 200
        self.ok = True

    def post(self):
        return


def test_checkout(project):
    project.checkout()
    o = check_output(["git", "-C", project.path, "rev-parse", "HEAD"])
    assert os.path.isdir(project.path)
    # checkout_output returns a byte string
    assert o.decode('utf-8').strip() == project.commit

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

def test_send_status(project, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'post', mock_get)
    project.send_status('success')
