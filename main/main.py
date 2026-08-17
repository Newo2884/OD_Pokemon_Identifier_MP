from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import *

main_bp = Blueprint("main", __name__, url_prefix="/main", template_folder="templates")
