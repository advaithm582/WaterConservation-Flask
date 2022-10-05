# This file is part of MyPHP.

# MyPHP is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free 
# Software Foundation, either version 3 of the License, or (at your 
# option) any later version.

# MyPHP is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.

# You should have received a copy of the GNU General Public License along
# with MyPHP. If not, see <https://www.gnu.org/licenses/>. 

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
    IntegerField,
    DateTimeField,
    TextAreaField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    InputRequired,
    Email,
    EqualTo
)

from app import db
from app.models import AMSDCApp


class AppAddingForm(FlaskForm):
    uniqname = StringField("Enter the UNIQUE name:", validators=[DataRequired()])
    name = StringField("Enter the App name:", validators=[DataRequired()])
    released = DateTimeField("Enter the date of release:")
    lastupdated = DateTimeField("Last updated on:")
    latestver = StringField("Latest version #")
    license = StringField("License")
    programming_lang = StringField("Programming Language")
    lang = StringField("Communication Language (e.g English)")
    type = StringField("Type")
    copyright = StringField("Copyright")
    repository = StringField("Repo link")
    installer = StringField("Installer")
    shortdesc = StringField("What is it? (500 chars)")
    longdesc = TextAreaField("Long description")
    
    submit = SubmitField('Submit')
    
    def validate_uniqname(self, username):
        if AMSDCApp.query.filter_by(uniqname=username.data).first():
                raise ValidationError('Application name is reserved!!')


class AppEditingForm(FlaskForm):
    # uniqname = StringField("Enter the UNIQUE name:", validators=[DataRequired()])
    name = StringField("Enter the App name:", validators=[DataRequired()])
    released = DateTimeField("Enter the date of release:")
    lastupdated = DateTimeField("Last updated on:")
    latestver = StringField("Latest version #")
    license = StringField("License")
    programming_lang = StringField("Programming Language")
    lang = StringField("Communication Language (e.g English)")
    type = StringField("Type")
    copyright = StringField("Copyright")
    repository = StringField("Repo link")
    installer = StringField("Installer")
    shortdesc = StringField("What is it? (500 chars)")
    longdesc = TextAreaField("Long description")
    
    submit = SubmitField('Submit')
    