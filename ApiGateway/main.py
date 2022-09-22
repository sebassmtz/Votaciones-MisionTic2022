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


@app.before_request
def before_request_callback():
    endPoint = clean_url(request.path)
    excludeRoutes = ['/login']
    if excludeRoutes.__contains__(request.path):
        print("ruta excluida",request.path)
        pass
    elif verify_jwt_in_request():
        user = get_jwt_identity()
        if user["rol"] is not None:
            havePermission = validate_permission(endPoint,request.method,user["rol"]["id"])
            if not havePermission:
               
                return jsonify({"message": "Permission denied"}),401
        else:
            return jsonify({"message": "Permission denied"}),401


def clean_url(url):
    parts = request.path.split("/")
    for part in parts:
        if re.search('\\d',part):
            url = url.replace(part,"?")
    return url

def validate_permission(route,method,role_id):
    url = dataConfig["url-backend-security"] + "/rol-permission/validate-permission/rol/" + str(role_id)
    print(url)
    isPermission = False
    body = {
        "url":route,
        "method": method
    }
    print(body)
    response = requests.get(url,json=body,headers=headers)
    try:
        data = response.json()
        if "_id" in data:
            isPermission = True
    except:
        pass
    return isPermission


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
    url = dataConfig["url-backend-votes"]+'/boards'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/boards", methods=['POST'])
def create_board():
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/boards'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)

@app.route("/boards/<string:id>", methods=['GET'])
def get_board(id):
    url = dataConfig["url-backend-votes"]+'/boards/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/boards/<string:id>", methods=['PUT'])
def update_board(id):
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/boards/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)
    
@app.route("/boards/<string:id>", methods=['DELETE'])
def delete_board(id):
    url = dataConfig["url-backend-votes"]+'/boards/'+id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

###########################################################
###              ENDPOINTS DE PARTIDOS                  ###
###########################################################
#Metodo para listar todos los partidos 
@app.route("/politicalPartys", methods=['GET'])
def get_political_partys():
    url = dataConfig["url-backend-votes"]+'/politicalPartys'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

#Metodo para mostrar un partido en especifico
@app.route("/politicalParty/<string:id>", methods=['GET'])
def get_political_party(id):
    url = dataConfig["url-backend-votes"]+'/politicalParty/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    
#Metodo para crear un partido
@app.route("/politicalParty", methods=['POST'])
def create_political_party():
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/politicalParty'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)
    
#Metodo para modificar un partido
@app.route("/politicalParty/<string:id>", methods=['PUT'])
def update_political_party(id):
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/politicalParty/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)
    
#Metodo para eliminar un partido
@app.route("/politicalParty/<string:id>", methods=['DELETE'])
def delete_political_party(id):
    url = dataConfig["url-backend-votes"]+'/politicalParty/'+id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

###########################################################
##              ENDPOINTS DE CANDIDATOS                 ###
###########################################################
@app.route("/candidates", methods=['GET'])
def get_candidates():
    url = dataConfig["url-backend-votes"]+'/candidates'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidates", methods=['POST'])
def create_candidate():
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/candidates'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)

@app.route("/candidates/<string:id>", methods=['GET'])
def get_candidate(id):
    url = dataConfig["url-backend-votes"]+'/candidates/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidates/<string:id>", methods=['PUT'])
def update_candidate(id):
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/candidates/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)

@app.route("/candidates/<string:id>", methods=['DELETE'])
def delete_candidate(id):
    url = dataConfig["url-backend-votes"]+'/candidates/'+id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidates/<string:id_candidato>/politicalParty/<string:id_partido>", methods=['PUT'])
def assign_party_to_candidate(id_candidato, id_partido ):
    data = request.get_json()
    url = dataConfig["url-backend-votes"]+'/candidates/'+id_candidato + "/politicalParty/"+id_partido
    response = requests.put(url, headers=headers)
    json = response.json()
    return jsonify(json)
    
#########################################################
####          ENDPOINTS DE RESULTADOS                ####
#########################################################

#OBTENER TODOS LOS RESULTADOS  
@app.route("/results", methods=['GET'])
def get_results():
    url = dataConfig["url-backend-votes"]+'/results'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    

#OBTENER UN RESULTADO EN ESPECIFICO
@app.route("/results/<string:id>", methods=['GET'])
def get_result(id):
    url = dataConfig["url-backend-votes"]+'/results/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    

#agregar un resultado en una mesa
@app.route("/results/board/<string:id_board>/candidate/<string:id_candidate>", methods=['POST'])
def create_result(id_board,id_candidate):
    data = {}
    url = dataConfig["url-backend-votes"]+'/results/board/'+id_board+"/candidate/"+id_candidate
    response = requests.post(url, json=data, headers=headers)
    json = response.json()
    return jsonify(json)
    

#actualizar un resultado
@app.route("/results/<string:id_result>/board/<string:id_board>/candidate/<string:id_candidate>",methods=['PUT'])
def update_result(id_result,id_board,id_candidate):
    url = dataConfig["url-backend-votes"]+'/results/'+id_result + "/board/"+id_board+"/candidate/"+id_candidate
    response = requests.put(url, headers=headers)
    json = response.json()
    return jsonify(json)
    

#Eliminar un resultado
@app.route("/results/<string:id>", methods=['DELETE'])
def delete_result(id):
    url = dataConfig["url-backend-votes"]+'/results/'+id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

################################################
#         ENDPOINT  DE LOS REPORTES            #
################################################

#Inscritos total en una mesa
@app.route("/reports/boards/<string:id_board>",methods=['GET'])
def sign_up_boards(id_board):
    url = dataConfig["url-backend-votes"]+'/reports/boards/'+id_board
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    

#Obtener las mesas en las que esta inscrito un candidato
@app.route("/reports/candidate/<string:id_candidate>",methods=['GET'])
def sign_up_boards_candidate(id_candidate):
    url = dataConfig["url-backend-votes"]+'/reports/candidate/'+id_candidate
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    

#Devuelve el numero de cédula mayor
@app.route("/reports/newIdentification",methods=['GET'])
def get_new_identification():
    url = dataConfig["url-backend-votes"]+'/reports/newIdentification'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    

 #Metodo para encontrar la mesa y el partido
@app.route("/reports/board/<string:id_board>/political/<string:id_party>",methods=['GET'])
def findBy_board_and_party(id_board, id_party):
    url = dataConfig["url-backend-votes"]+'/reports/board/' + id_board + '/political/'+ id_party
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
    
# ------------------------- Server -------------------------------

if __name__ == "__main__":
    url = "http://"+dataConfig["url-backend"]+":"+str(dataConfig["port"])
    print("Server running:" + url)
    serve(app, host = dataConfig["url-backend"], 
    port=dataConfig["port"])


