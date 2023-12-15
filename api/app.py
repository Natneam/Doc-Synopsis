import os
from flask import Flask, request, jsonify, abort

from utils.utils import csv_preprocessing, pdf_preprocessing, llm_pipeline

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

#file summarization endpoint
@app.route('/summarize/<filename>', methods=['GET'])
def summarize(filename):
    if "/" in filename:
        abort(400, "no subdirectories allowed")

    if filename.endswith(".pdf"):
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        summary = llm_pipeline(file_path, "pdf")
        return jsonify({"summary" : summary}), 200
    elif filename.endswith(".csv"):
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        summary = llm_pipeline(file_path, "csv")
        return jsonify({"summary" : summary}), 200
    else:
        return jsonify({"message" : "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
