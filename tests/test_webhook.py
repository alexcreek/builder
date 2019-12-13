import pytest
import json
from builder import webhook

@pytest.fixture
def app():
    return webhook.app

@pytest.fixture
def webhook_payload():
    with open('tests/payload.json', 'r') as f:
        p = json.load(f)
    return p

def test_ping(client):
    assert client.get('/ping').status_code == 200

def test_webhook(client, webhook_payload):
    assert client.post('/webhook', json=webhook_payload).status_code == 200
    assert client.post('/webhook').status_code == 400
    assert client.post('/webhook', json={}).status_code == 400
    


