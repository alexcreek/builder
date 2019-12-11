from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        return jsonify()
    else:
        abort(400)

@app.route('/ping')
def ping():
    return jsonify('pong')