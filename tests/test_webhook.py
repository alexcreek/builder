import json
import pytest
from builder import webhook

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

def test_webhook(client, webhook_payload):
 #  This has turned into an integration test.
 #  Disabling for the time being
 #   assert client.post('/webhook', json=webhook_payload).status_code == 200
    assert client.post('/webhook').status_code == 400
    assert client.post('/webhook', json={}).status_code == 400

def test_github_ping(client, github_ping_payload):
    assert client.post('/webhook', json=github_ping_payload).status_code == 200
