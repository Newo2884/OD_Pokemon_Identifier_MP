from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.String(200))
    egg_groups = db.Column(db.String(200), nullable=False)
    genders = db.Column(db.String(200), nullable=False)
    growth_rates = db.Column(db.String(200), nullable=False)
    natures = db.Column(db.String(200), nullable=False)
    locations = db.Column(db.Text, nullable=False)
    colours = db.Column(db.String(200), nullable=False)
    forms = db.Column(db.String(200), nullable=False)
    habitats = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    class_id = db.Column(db.String(50), unique=True)

    def make_json(self):
        data = {
                "name" : self.name,
                "type" : self.type,
                "desc" : self.desc,
                }
        return data
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    user = db.relationship("User", backref="collections", lazy=True)
    pokemon = db.relationship("Pokemon", backref="collections", lazy=True)