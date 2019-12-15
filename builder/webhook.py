from logging import getLogger
from flask import Flask, request, jsonify, abort
import builder.utils
from builder.project import Project

# setup logging
builder.utils.setup_logger('webhook')
logger = getLogger('webhook')

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        logger.info('this is going to flask logs')
        data = request.json
        try:
            p = Project(data['repository']['clone_url'],
                        data['after'],
                        data['ref'])
        except KeyError as e:
            logger.error('Paylod missing key %s', e)
            return abort(400)
        p.start()
        return jsonify(request.json)
    return abort(400)

@app.route('/ping')
def ping():
    return jsonify('pong')
