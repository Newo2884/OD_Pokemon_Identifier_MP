from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from models import db, User, Pokemon, Collection
import json, os

from main.main import main_bp
from auth.auth import auth_bp

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = "INSERTACTUALSECRETKEYHERE"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir}/pokelist.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

def seed_database():
    try:
        with open ("pokedex.json", "r", encoding="utf-8") as f:
            pokedex = json.load(f)

            for key, data in pokedex.items():
                exists = Pokemon.query.filter_by(name=data["name"]).first()
                if not exists:
                    new_pokemon = Pokemon(
                        name=data.get("name")("english"),
                        id=data.get("id"),
                        type=data.get("type"),
                        ability=data.get("profile")("ability"),
                        egg=data.get("profile")("egg"),
                        evolution=data.get("evolution"),
                        decription=data.get("decription")
                    )
                    db.session.add(new_pokemon)

            db.session.commit()
            print("Successfully added all Pokemon data")
    except Exception as e:
        print(f"Error adding all Pokemon data: {e}")
        db.session.rollback()

@app.route("/", methods = ['GET', 'POST'])
def index():
   return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, host="0.0.0.0")