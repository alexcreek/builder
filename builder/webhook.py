import sys
import time
from flask import Flask, request, jsonify, abort

from builder.project import Project
from multiprocessing import Process, active_children

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

        mp = Process(target=p.process, args=())
        #mp.daemon = True
        mp.start()
        
        #mp.join()
        #p.clone_repo()
        # parse build manifest
        # run test
        # build
        return jsonify(request.json)
    else:
        abort(400)

@app.route('/ping')
def ping():
    return jsonify('pong')