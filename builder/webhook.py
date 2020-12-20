import os
import hmac
from logging import getLogger
from flask import Flask, request, jsonify, abort
import builder.common
from builder.project import Project

# setup logging
builder.common.setup_logger('webhook')
logger = getLogger('webhook')

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    logger.info('Webhook recieved')
    if request.is_json:
        verify_signature(request)
        data = request.json
        # Attempt processing github pings first
        try:
            github_ping(data['zen'],
                        data['hook_id'],
                        data['hook']['test_url'])
            return jsonify("{}")
        except KeyError as e:
            pass

        # Attempt to build 
        try:
            build(data['repository']['clone_url'],
                  data['after'],
                  data['ref'],
                  data['repository']['statuses_url'])
            return jsonify("{}")
        except KeyError as e:
            logger.error('Paylod missing key %s', e)
            return abort(400)
    return abort(400)

@app.route('/ping')
def ping():
    return jsonify('pong')

def build(url, commit, branch, status_url):
    p = Project(url, commit, branch, status_url)
    logger.info('Build started')
    p.start()

def verify_signature(payload):
    h = hmac.new(os.environb[b'SECRET'], digestmod='sha1')
    h.update(payload.data)
    if not hmac.compare_digest(h.hexdigest(), payload.headers.get('X-Hub-Signature').replace('sha1=', '')):
        return abort(500)
