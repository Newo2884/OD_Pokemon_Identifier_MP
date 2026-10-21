from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask_login import LoginManager, current_user
from models import db, User, Pokemon, Collection
import json, os, requests, io, time
from io import BytesIO
from PIL import Image

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

def pokemon_image_url_to_blob(image_url):
    try:        
        if not image_url or not image_url.lower().startswith(("http://", "https://")):
            raise ValueError(f"No record found {image_url}")

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        with Image.open(BytesIO(response.content)) as img:
            img.load()
            img = img.convert("RGBA")
        
            png_buffer = BytesIO()
            img.save(png_buffer, format="PNG")

            return png_buffer.getvalue()
    
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
    except (OSError, ValueError) as e:
        print(f"Error processing image: {e}")
    return None

def seed_database():
    try:
        with open ("pokedex.json", "r", encoding="utf-8") as f:
            pokedex = json.load(f)
            
            for index, data in enumerate(pokedex, start=1):
                name=data.get("name", {}).get("english")
                image_url=data.get("image", {}).get("thumbnail")

                exists = Pokemon.query.filter_by(name=name).first()

                if exists:
                    print(f"[{index}/{len(pokedex)}] Skipping {name}: already exists")
                    continue

                print(f"[{index}/{len(pokedex)}] Downloading image for {name}")

                png_blob=pokemon_image_url_to_blob(image_url)

                if png_blob is None:
                    print("Could not download image or conversion failed")
                    raise ValueError("Unable to download or convert image")

                if not exists:
     
                    new_pokemon = Pokemon(
                        name=name,
                        id=data.get("id"),
                        type=", ".join(data.get("type", [])),
                        ability=", ".join(
                            f"{ability[0]} (hidden)" if ability[1] == "true" else ability[0]
                            for ability in data.get("profile", {}).get("ability", [])),
                        egg=", ".join(data.get("profile", {}).get("egg", [])),
                        evolution=json.dumps(data.get("evolution", {})),
                        description=data.get("description", ""),
                        image_url=image_url,
                        image_data=png_blob,
                    )
                    db.session.add(new_pokemon)

                    print(f"Added {name}: {len(png_blob)} image bytes")

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
    app.run(debug=True, #host="0.0.0.0"
            )