import os
import json
import pytest
from builder.project import Project
from builder import webhook

os.environ['GH_USER'] = 'testuser'
os.environ['GH_TOKEN'] = 'testtoken'
os.environ['SECRET'] = 'burrow'

url = 'git@github.com:alexcreek/builder.git'
commit = '6a9d4aeee29927ca4baed7d67f8ba4eb548bf10b'
branch = 'refs/heads/test_fixture'
status_url = 'https://api.github.com/repos/alexcreek/builder/statuses/{sha}'

# for each fixture used by a test function there is typically a parameter
# (named after the fixture) in the test function’s definition
# https://docs.pytest.org/en/stable/fixture.html

@pytest.fixture
def app():
    return webhook.app

@pytest.fixture
def webhook_payload():
    with open('tests/payload.json', 'r') as f:
        p = json.load(f)
    return p

@pytest.fixture
def github_ping_payload():
    with open('tests/github_ping.json', 'r') as f:
        p = json.load(f)
    return p

@pytest.fixture
def project():
    p = Project(url, commit, branch, status_url)
    return p
