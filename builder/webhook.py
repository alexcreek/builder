import sys
from flask import Flask, request, jsonify, abort

from builder.project import Project

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.json
        print(data['ref'], file=sys.stderr)
        print(data['after'], file=sys.stderr)
        print(data['repository']['clone_url'], file=sys.stderr)

        p = Project(data['repository']['clone_url'],
                    data['after'],
                    data['ref'])

        p.clone_repo()
        p.cleanup()
        # parse build manifest
        # run test
        # build

        return jsonify(request.json)
    else:
        abort(400)

@app.route('/ping')
def ping():
    return jsonify('pong')