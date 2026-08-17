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
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir}/tcg.db"
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
        with open ("something.json", "r") as f:
            something = json.load(f)

            for key, data in something.items():
                exists = Pokemon.query.filter_by(name=data["name"]).first()
                if not exists:
                    new_pokemon = Pokemon(
                        name=data.get("name")
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