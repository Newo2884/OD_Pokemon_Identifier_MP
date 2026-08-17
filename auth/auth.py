from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from sqlalchemy import func

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter(
            func.lower(User.email) == request.form["email"].lower()
        ).first()
        print(user)
        if user:
            if check_password_hash(user.password, request.form["password"]):
                # success
                login_user(user)
                flash("Logged in as " + user.username, "success")
                return redirect(url_for("main.index"))
            else:
                flash("Invalid password", "danger")
        else:
            flash("Invalid email", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashedPass = generate_password_hash(request.form["password"])
        newUser = User(
            username = request.form["username"],
            password = hashedPass,
            email = request.form["email"],
        )
        db.session.add(newUser)
        db.session.commit()
        flash("Account created, please log in", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    flash("Successfully logged out", "success")
    logout_user()
    return redirect(url_for("auth.login"))