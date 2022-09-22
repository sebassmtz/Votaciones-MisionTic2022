from urllib import response
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

def clean_url():
    parts = request.path.split('/')
    url = request.path
    for part in parts:
        if re.search('\\d',part):
            url = url.replace(part,"?")
    return url

def validate_permission(route,role_id,method):
    url = dataConfig["url-backend-security"] + "/rol-permission/validate-permission/rol/" + str(role_id)
    isPermission = False
    body = {"url":route, "method": method}
    response = requests.post(url,json=body,headers=headers)
    try:
        data = response.json()
        if "_id" in data:
            isPermission = True
    except:
        pass
    return isPermission

@app.before_request
def before_request_callback():
    endPoint = cleanURL = clean_url(request.path)
    excludeRoutes = ['/login']
    if excludeRoutes.__contains__(request.path):
        print("ruta excluida",request.path)
        pass
    elif verify_jwt_in_request():
        user = get_jwt_identity()
        if user["rol"] is not None:
            havePermission = validate_permission(endPoint,request.method,user["rol"]["_id"])
            if not havePermission:
                return jsonify({"message": "Permission denied"}),401
        else:
            return jsonify({"message": "Permission denied"}),401


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

###########################################################
################# ENDPOINTS DE MESAS ######################
###########################################################
@app.route("/boards", methods=['GET'])
def get_boards():
    url = dataConfig["url-backend-votes"]+'/zrk5nkf/boards'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/boards", methods=['POST'])
def create_board():
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/zrk5nkf/boards'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)

@app.route("/boards/<string:id>", methods=['GET'])
def get_board(id):
    url = dataConfig["url-backend-votes"]+'/zrk5nkf/boards/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/boards/<string:id>", methods=['PUT'])
def update_board(id):
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/zrk5nkf/boards/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)
    
@app.route("/boards/<string:id>", methods=['DELETE'])
def delete_board(id):
    url = dataConfig["url-backend-votes"]+'/zrk5nkf/boards/'+id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)


# ------------------------- Server -------------------------------

if __name__ == "__main__":
    url = "http://"+dataConfig["url-backend"]+":"+str(dataConfig["port"])
    print("Server running:" + url)
    serve(app, host = dataConfig["url-backend"], 
    port=dataConfig["port"])


