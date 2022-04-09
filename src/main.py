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
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#ENDPOINTS

#Get all characters
@app.route('/characters',methods=['GET'])
def get_all_characters():
    all_characters = []
    characters = Character.query.all()
    for character in characters:
        all_characters.append(character.serialize())
    return jsonify(all_characters), 200

#Get character
@app.route('/characters/<character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

#Get all planets
@app.route('/planets',methods=['GET'])
def get_all_planets():
    all_planets = []
    planets = Planet.query.all()
    for planet in planets:
        all_planets.append(planet.serialize())
    return jsonify(all_planets), 200

#Get planet
@app.route('/planets/<planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

#Get all users
@app.route('/users',methods=['GET'])
def get_all_users():
    all_users = []
    users = User.query.all()
    for user in users:
        all_users.append(user.serialize())
    return jsonify(all_users), 200

#Get user
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user=User.query.get(user_id)
    return jsonify(user.serialize()), 200

#Get user favourites
@app.route('/<user_id>/favorites',methods=['GET'])
def get_user_favorites(user_id):
    favorites_list = []
    favorites = Favorite.query.filter(Favorite.user_id==user_id)
    for favorite in favorites:
        favorites_list.append(favorite.serialize())
    return jsonify(favorites_list), 200

#Post new favourite planet
@app.route('/favorites/planets', methods=['POST'])
def new_favorite_planet():
    body = request.get_json()
    new_fav_planet = Favorite(planet_id = body['planet_id'], user_id = body['user_id'])
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify(new_favorite_planet.serialize()), 200

#Post new favourite character
@app.route('/favorites/characters', methods=['POST'])
def new_favorite_character():
    body = request.get_json()
    new_fav_character = Favorite(character_id = body['character_id'], user_id = body['user_id'])
    db.session.add(new_favorite_character)
    db.session.commit()
    return jsonify(new_favorite_character.serialize()), 200

#Delete fav planet
@app.route('/<user_id>/favorites/planets/<planet_id>', methods=['DELETE'])
def delete_planet_favourite(user_id, planet_id):
    Favorite.query.filter(Favorite.planet_id == planet_id).delete()
    db.session.commit()
    return jsonify('The planet has been successfully removed from favourites'), 200

#Delete fav character
@app.route('/<user_id>/favorites/characters/<character_id>', methods=['DELETE'])
def delete_favourite_char(user_id, character_id):
    Favorite.query.filter(Favorite.character_id == character_id).delete()
    db.session.commit()
    return jsonify('The character has been successfully removed from favourites'), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
