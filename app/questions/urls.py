from app.questions import bp
from app.questions import views as v

bp.add_url_rule("/", endpoint="list", view_func=v.list_questions)
bp.add_url_rule("/add",)