from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField, 
    SubmitField, 
    TextAreaField,
    SelectField
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
# from flask_babel import _, lazy_gettext as _l
from app.models import Question

class AddTopicForm(FlaskForm):
    #title = StringField('Question Title', validators=[DataRequired()])
    text = StringField('Topic name', validators=[DataRequired()])
    desc = TextAreaField('Topic description', validators=[DataRequired()])
    submit = SubmitField('Add Topic')

class AddQuestionForm(FlaskForm):
    #title = StringField('Question Title', validators=[DataRequired()])
    topic = SelectField('Topic', choices=[], validators=[DataRequired()])
    text = TextAreaField('Question Body', validators=[DataRequired()])
    submit = SubmitField('Add Question')

class DeleteQuestionForm(FlaskForm):
    confirmation = StringField("Type 'I am sure' here to proceed without the quotes",
         validators=[DataRequired()])
    submit = SubmitField('Delete Question')