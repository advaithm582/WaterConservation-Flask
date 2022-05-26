from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField, 
    SubmitField, 
    TextAreaField
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
# from flask_babel import _, lazy_gettext as _l
from app.models import Announcement

class EditAnnouncementForm(FlaskForm):
    title = StringField('Announcement Title', validators=[DataRequired()])
    body = TextAreaField('Announcement Body', validators=[DataRequired()])
    submit = SubmitField('Update Announcement')

class AddAnnouncementForm(FlaskForm):
    title = StringField('Announcement Title', validators=[DataRequired()])
    body = TextAreaField('Announcement Body', validators=[DataRequired()])
    submit = SubmitField('Add Announcement')

class DeleteAnnouncementForm(FlaskForm):
    confirmation = StringField("Type 'I am sure' here to proceed without the quotes",
         validators=[DataRequired()])
    submit = SubmitField('Delete Announcement')