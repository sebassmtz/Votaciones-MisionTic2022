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

# ------------------------- Setting Flask App -------------------------------

app = Flask(__name__)
cors = CORS(app)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

dataConfig = loadFileConfig()

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

headers = {"Content-Type": "application/json; charset=utf-8"}

# ------------------------- Middleware -------------------------------



# ------------------------- Endpoints -------------------------------

@app.route("/", methods=["GET"])
def test():
    json = {}
    json["message"] = "Server Running..."
    return jsonify(json)

@app.route("/login",methods=['POST'])
def create_token():
    data = request.get_json()
    url = dataConfig["url-backend-security"] + "/users/validate"
    response = requests.post(url, json=data,headers=headers)
    if response.status_code == 401:
        return jsonify({"msg": "Usuario o contrasena Incorrectos"}), 401
    elif response.status_code == 500:
        return jsonify({"msg": "Error inseperado"}), 500
    elif response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60*60*24)
        access_token = create_access_token(identity=user,expires_delta=expires)
        return jsonify({"token": access_token, "user_id":user["id"]})



# ------------------------- Server -------------------------------

if __name__ == "__main__":
    url = "http://"+dataConfig["url-backend"]+":"+str(dataConfig["port"])
    print("Server running:" + url)
    serve(app, host = dataConfig["url-backend"], 
    port=dataConfig["port"])


