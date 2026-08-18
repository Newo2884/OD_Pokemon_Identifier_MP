from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    ability = db.Column(db.String(200))
    egg = db.Column(db.String(200))
    evolution = db.Column(db.String(200))
    decription = db.Column(db.Text, nullable=False)
    class_id = db.Column(db.String(50), unique=True)

    def make_json(self):
        data = {
                "name" : self.name,
                "type" : self.type,
                "ability" : self.type,
                "egg_groups" : self.type,
                "evolution" : self.type,
                "decription" : self.decription,
                }
        return data
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False, unique=True)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    
    user = db.relationship("User", backref="collections", lazy=True)
    pokemon = db.relationship("Pokemon", backref="collections", lazy=True)