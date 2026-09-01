from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import *

main_bp = Blueprint("main", __name__, template_folder="templates")

# currenty the only way to add pokemon to collections after trialing how to for a while (I know it shares the same directory as the one in app.py but nothing wrong seems to have happened from it)
@main_bp.route("/", methods = ['GET', 'POST'])
def index():
    # same kind of form function as logging in and registering
    if request.method == 'POST':
        new_pokemon = Collection(
            user_id = current_user.id,
            pokemon_id = request.form["pokemon_id"],
        )
    
        db.session.add(new_pokemon)
        db.session.commit()
        flash("Pokemon added to collection", "success")
        return redirect(url_for("main.view_collection", user_id = current_user.id))
    
    return render_template("index.html")

# will become the main way of adding pokemon to collections once the machine learning part is done

@main_bp.route("/add_to_collection", methods=['POST'])
#def add_to_collection():
#    data = request.json
#    user_id = current_user.id
#    pokemon_id = data.get("pokemon_name")
#
#    user = User.query.get(user_id)
#    pokemon = Pokemon.query.filter_by(id=pokemon_id).first()
#
#    if not user or not pokemon:
#        return jsonify({"success": False, "error": "User or pokemon not found"}), 404
#
    # Check if the user already has this pokemon in their collection
#    existing_entry = Collection.query.filter_by(user_id=user_id, pokemon_id=pokemon.id).first()
#    if existing_entry:
#        existing_entry.quantity += 1
#    else:
#        new_entry = Collection(user_id=user_id, pokemon_id=pokemon.id)
#        db.session.add(new_entry)
#
#    db.session.commit()
#    return jsonify({"success": True, "message": "Pokemon added to collection"})

# allows the user to go to collection.html and see their identified Pokemon

@main_bp.route("/collection/<int:user_id>", methods=["GET"])
def view_collection(user_id):
    c = Collection.query.filter_by(user_id=user_id).all()
    return render_template("collection.html", collection = c)