from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response, abort
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

    flash("Pokemon ID or Name does not exist", "danger")
    return render_template("index.html")

# will become the main way of adding pokemon to collections once the machine learning part is done

#@main_bp.route("/add_to_collection", methods=['POST'])
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
    collection = Collection.query.filter_by(user_id=user_id).join(Pokemon).order_by(Pokemon.id.asc()).all()

    for entry in collection:
        entry.evolution_info = get_evolution_info(entry.pokemon)

#    add a way for pokeball or silhoutte images of the pokemon to signify have not identified - unlikely to be added
#    add for loop that will enable pokemon evolutions to be readable not just the json.dump info
    return render_template("collection.html", collection = collection, entry = entry)

@main_bp.route("/pokemon/image/<int:pokemon_id>")
def pokemon_image(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    if not pokemon.image_data:
        abort(404)

    return Response(pokemon.image_data, mimetype="image/png")

def find_pokemon_by_id(pokemon_id):
    try:
        return Pokemon.query.filter_by(id = int(pokemon_id)).first()
    except (ValueError, TypeError):
        return None

def get_evolution_info(pokemon):

    evolution = json.loads(pokemon.evolution or "{}")
    
    #try:
    #    evolution = json.loads(pokemon.evolution) if pokemon.evolution else {}
    #except (json.JSONDecodeError, TypeError):
    #    evolution = {}

    result = {"previous": None, "next": []}

    previous = evolution.get("prev")

    if previous:
        previous_pokemon = Pokemon.query.get(int(previous[0]))

        if previous_pokemon:
            result["previous"] = {"id": previous_pokemon.id, "name": previous_pokemon.name, "condition": previous[1]}

    for evo in evolution.get("next") or []:

        next_pokemon = Pokemon.query.get(int(evo[0]))

        if next_pokemon:
            result["next"].append({"id": next_pokemon.id, "name": next_pokemon.name, "condition": evo[1]})

    return result