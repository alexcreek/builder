import os
import json
import pytest
from flask import request
from werkzeug.exceptions import InternalServerError
from builder import webhook

os.environ['SECRET'] = 'burrow'

# https://pytest-flask.readthedocs.io/en/latest/features.html?highlight=headers#request-ctx-request-context

class MockRequest():
    def __init__(self, data, headers):
        self.data = json.dumps(data).encode('utf-8')
        self.headers = headers


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

def test_ping(client):
    assert client.get('/ping').status_code == 200

def test_webhook_requires_json(client, webhook_payload):
    assert client.post('/webhook').status_code == 400

def test_verify_signature(webhook_payload):
    req = MockRequest(webhook_payload, {'X-Hub-Signature': 'sha1=f72b257a9c1bc1a2c508f06e18d59da780c3412e'})
    webhook.verify_signature(req)

    with pytest.raises(InternalServerError) as e:
        bad_req = MockRequest(webhook_payload, {'X-Hub-Signature': 'sha1=123456'})
        webhook.verify_signature(bad_req)
    assert e.type == InternalServerError

def test_github_ping(client, github_ping_payload):
    assert client.post('/webhook', json=github_ping_payload,
                       headers=[('X-Hub-Signature', 'sha1=eec3d1c560534e2608bed790b272f4c8507d6500')]
                       ).status_code == 200

# This triggers the whole workflow and ends up being an integration test
# Pytest throws 'ValueError: I/O operation on closed file' errors
# This may not be something for pytest to run
#def test_webhook(client, webhook_payload):
#    assert client.post('/webhook', json=webhook_payload,
#                       headers=[('X-Hub-Signature', 'sha1=8595a0b1f5dc7d2464a7bb108e3633cc301568bb')]
#                       ).status_code == 200
