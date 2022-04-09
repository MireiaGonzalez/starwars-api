from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    diameter = db.Column(db.Integer )
    rotation_period = db.Column(db.Integer )
    orbital_period = db.Column(db.Integer )
    gravity = db.Column(db.String(80))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(20))
    terrain = db.Column(db.String(20))
    surface_water = db.Column(db.Integer)
    url = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "url": self.url
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)    
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    homeworld = db.Column(db.String(50))
    url = db.Column(db.String(250))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship('Planet', backref='character')

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "url": self.url,
            "planet_id": self.planet_id,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet = db.relationship('Planet', backref="favorite")
    character = db.relationship('Character', backref="favorite")
    user = db.relationship('User', backref="favorite")

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return{
            "id": self.id,
            "planet_id": self.planet_id,
            "character": self.character.serialize(),
            "user": self.user.serialize()
        }