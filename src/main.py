"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Fav_Planet, Fav_Character

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def Get_Planets():
    planets = list(map(lambda planet: planet.serialize(), Planet.query.all()))
    return jsonify(results = planets), 200 

@app.route('/planets/<int:planet_id>', methods=['GET'])
def Get_Planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200     

@app.route('/people', methods=['GET'])
def Get_People():
    characters = list(map(lambda p: p.serialize(), Character.query.all()))
    return jsonify(results = characters), 200     

@app.route('/people/<int:people_id>', methods=['GET'])
def Get_Person(people_id):
    print("ID GET PEOPLE: ", people_id)
    character = Character.query.get(people_id)
    print("Character: ", character)
    return jsonify(character.serialize()), 200    

@app.route('/users', methods=['GET'])
def Get_Users():
    users = list(map(lambda p: p.serialize(), User.query.all()))
    return jsonify(users), 200   

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
#@jwt_required()
def Get_User_Fav(user_id):
    print("hola desde> Get_User_Fav")
    user = User.query.get(user_id)
    favs = list(map(lambda p: p.serialize(), user.Fav_Character)) + list(map(lambda p: p.serialize(), user.Fav_Planet))
    return jsonify(favs), 200  

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
#@jwt_required()
def POST_User_Fav(user_id):
    print("hola desde> POST_User_Fav")
    tipo = request.json.get("tipo", None)
    id = request.json.get("id", None)

    if tipo == "planet":
        favPlanet = Fav_Planet(user_id=user_id, planet_id=id)
        db.session.add(favPlanet)
        db.session.commit()

        return jsonify(favPlanet.serialize()), 200   
    elif tipo == "people":
        favPeople = Fav_Character(user_id=user_id, character_id=id)
        db.session.add(favPeople)
        db.session.commit()

        return jsonify(favPeople.serialize()), 200  

    return APIException("BadRequest", status_code=400)

@app.route('/favorite/<string:tipo>/<int:favorite_id>', methods=['DELETE'])
#@jwt_required()
def DELETE_User_Fav(tipo, favorite_id):
    print("hola desde> DELETE_User_Fav")
    print("hola desde> DELETE_User_Fav", tipo)
    print("hola desde> DELETE_User_Fav", favorite_id)
    if tipo == "planet":
        fav_to_del = Fav_Planet.query.filter_by(id=favorite_id).first()
        if fav_to_del is None:
            return "Not Found", 404
        else:
           db.session.delete(fav_to_del)
           db.session.commit()      
           return jsonify(fav_to_del.serialize()), 200         
    elif tipo == "people":
        fav_to_del = Fav_Character.query.filter_by(id=favorite_id).first()
        print(fav_to_del)
        if fav_to_del is None:
            return "Not Found", 404
        else:
            db.session.delete(fav_to_del)
            db.session.commit()
            return jsonify(fav_to_del.serialize()), 200           
    
    return "Bad Request", 400
      

@app.route('/token', methods=['POST'])
def CreateToken(): 
    if request.method == "POST":
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            # the user was not found on the database
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=user.id)
        return jsonify({ "token": access_token, "user_id": user.id })
    else:
        return "Hello"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
