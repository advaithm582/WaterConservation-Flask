from flask import Blueprint

# This is announcements blueprint
bp = Blueprint('announcements', __name__)

from app.announcements import routes