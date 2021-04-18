from flask_sqlalchemy import SQLAlchemy

# Crear una base de datos previamente configurada
# Regresa un objeto
# Model, Column, Integer, String, Datetime, Boolean
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)
    name = db.Column(db.String(250), nullable=True)

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<Planet %r>' % self.name

     # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited,
            "name": self.name
        }

class Character(db.Model):
    __tablename__ = 'character'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    birth_year = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)  

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<Character %r>' % self.name

     # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "name": self.name,
            "created": self.created,
            "edited": self.edited
        }

class Fav_Planet(db.Model):
    __tablename__ = 'fav_planet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = db.relationship("User", lazy='subquery', backref=db.backref("Fav_Planet", cascade="all,delete"))
    planet = db.relationship("Planet", lazy='subquery', backref=db.backref("Fav_Planet", cascade="all,delete"))

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "content": self.planet.serialize()

        }

class Fav_Character(db.Model):
    __tablename__ = 'fav_character'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user = db.relationship("User", lazy='subquery', backref=db.backref("Fav_Character", cascade="all,delete"))
    character = db.relationship("Character", lazy='subquery', backref=db.backref("Fav_Character", cascade="all,delete"))

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "content": self.character.serialize()
        }