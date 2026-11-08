from flask import Blueprint, render_template, redirect, url_for, request, flash, Response, abort
from flask_login import current_user
from models import *

main_bp = Blueprint("main", __name__, template_folder="templates")

@main_bp.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':

        # identify the pokemon
        identify_pokemon = request.form["pokemon_id"].strip()

        #checks if it is a digit/numeral/integer or a string
        if identify_pokemon.isdigit():
            pokemon = Pokemon.query.get(int(identify_pokemon))
        else:
            pokemon = Pokemon.query.filter(db.func.lower(Pokemon.name) == identify_pokemon.lower()).first()

        if pokemon:

            # checks if it exists and if it does then it will flash a warning message and return to the index page - may be able to amke it just refresh the page instead of a full reload/redirect
            existing_pokemon = Collection.query.filter_by(user_id = current_user.id, pokemon_id = pokemon.id).first()
            if existing_pokemon:
                flash("You have already identified and added this Pokemon to your collection.", "danger")
                return redirect(url_for("main.index"))
            else:

                # adds the pokemon data to the collection
                new_pokemon = Collection(
                    user_id = current_user.id,
                    pokemon_id = pokemon.id
                )

                db.session.add(new_pokemon)
                db.session.commit()
                flash("Added Pokemon to your collection!", "success")
                return redirect(url_for("main.view_collection", user_id = current_user.id))
        
        else:
            flash("Please use a valid Pokemon ID number or name", "danger")
            return redirect(url_for("main.index", user_id = current_user.id))
    else:
        return render_template("index.html")

@main_bp.route("/collection/<int:user_id>", methods=["GET"])
def view_collection(user_id):
    #allows the data in the collection table of the database be used by the collection html and viewed by the user
    collection = Collection.query.filter_by(user_id=user_id).join(Pokemon).order_by(Pokemon.id.asc()).all()

    for entry in collection:
        entry.evolution_info = get_evolution_info(entry.pokemon)

#    add a way for pokeball or silhoutte images of the pokemon to signify have not identified - unlikely to be added
#    pokeball image is done - silhouette will not happen
    return render_template("collection.html", collection = collection, entry = entry)

#   allows the blob image in database to be used and viewed
@main_bp.route("/pokemon/image/<int:pokemon_id>")
def pokemon_image(pokemon_id):
    pok_img = Pokemon.query.get_or_404(pokemon_id)
    if not pok_img.image_data:
        abort(404)

    return Response(pok_img.image_data, mimetype="image/png")

#    used to get and convert the json.dumps information on a pokemons evolution/s and devolution into an easy to read state
def get_evolution_info(pokemon):

    evolution = json.loads(pokemon.evolution or "{}")

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