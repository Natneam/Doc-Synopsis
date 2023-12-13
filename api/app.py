import os
from flask import Flask, request, jsonify, abort

UPLOAD_DIRECTORY = "./data"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


app = Flask(__name__)


#file upload endpoint
@app.route('/upload/<filename>', methods=['POST'])
def upload(filename):
    if "/" in filename:
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.files['file'].read())

    return jsonify({"message" : "File successfully uploaded"}), 201

if __name__ == '__main__':
    app.run(debug=True)
