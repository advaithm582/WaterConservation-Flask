from flask import Blueprint

# This is auth blueprint
bp = Blueprint('user_management', __name__)

from app.user_management import urls