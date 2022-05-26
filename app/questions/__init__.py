from flask import Blueprint

# This is announcements blueprint
bp = Blueprint('questions', __name__)

from app.questions import urls