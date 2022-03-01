import tempfile
import pandas as pd
import awsgi
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response, send_file
import logging

app = Flask(__name__)
CORS(app)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route("/text", methods=["POST"])
def get_plain_text():
    return jsonify("hello world")


@app.route("/excel_file", methods=["POST"])
def get_excel():
    filename = f'{tempfile.gettempdir()}/dummy.xlsx'
    df = pd.DataFrame({"A": ["a", "b", "a"], "B": [
                      "b", "a", "c"], "C": [1, 2, 3]})

    writer = pd.ExcelWriter(filename, engine='openpyxl')
    df.to_excel(writer)
    writer.save()
    return send_file(filename, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
