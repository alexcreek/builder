import sys
import time
from logging import getLogger
from flask import Flask, request, jsonify, abort
from builder.project import Project
import builder.utils

# setup logging
builder.utils.init_logging('webhook')
logger = getLogger('webhook')

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        #print('this is going to flask logs', file=sys.stderr)
        logger.info('this is going to flask logs')
        #log('not sure where this is going')
        data = request.json
        p = Project(data['repository']['clone_url'],
                    data['after'],
                    data['ref'])
        p.start()
        return jsonify(request.json)
    else:
        abort(400)

@app.route('/ping')
def ping():
    return jsonify('pong')
