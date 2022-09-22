from flask import Flask
from flask import jsonify, request
import requests
from flask_cors import CORS
from waitress import serve
import datetime
import re
import json

from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods=["GET"])
def test():
    json = {}
    json["message"] = "Server Running..."
    return jsonify(json)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    dataConfig = loadFileConfig()
    print("Server running: http://"+dataConfig["url-backend"]+
    ":"+str(dataConfig["port"]))
    serve(app, host = dataConfig["url-backend"], 
    port=dataConfig["port"])


