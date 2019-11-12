import os
from flask import Flask, request, make_response, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


root_directory = "/objects/"


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per minute", "1 per second"],
)

@app.route('/', methods=['GET'])
def get_all():
    return make_response(jsonify(os.listdir(root_directory)), 200)

@app.route('/', methods=['DELETE'])
@limiter.limit("1 per hour")
def delete_all():
    for file in os.listdir(root_directory):
        os.remove(root_directory + file)
    return '', 200

@app.route('/objs/<string:obj_id>', methods=['GET'])
def retieve(obj_id):
    if obj_id in os.listdir(root_directory):
        with open(root_directory + obj_id, 'rb') as f:
            return make_response(f.read(), 200)
    else:
        abort(404)

@app.route('/objs/<string:obj_id>', methods=['PUT'])
def store(obj_id):
    with open(root_directory + obj_id, 'wb') as f:
        f.write(request.data)
    return '', 200

@app.route('/objs/<string:obj_id>', methods=['DELETE'])
def remove(obj_id):
    if obj_id in os.listdir(root_directory):
        os.remove(root_directory + obj_id)
        return '', 200
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
