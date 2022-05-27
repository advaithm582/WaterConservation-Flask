from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
    IntegerField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    InputRequired,
    Email,
    EqualTo
)


class WaterSavingForm(FlaskForm):
    no_of_taps = IntegerField('Enter the number of taps in your house?', 
                             validators=[InputRequired()])
    no_of_ltaps = IntegerField('Enter the number of leaky taps in your house?', 
                             validators=[InputRequired()])
    t_flowrate = IntegerField('Enter the flow rate of these taps in L/min', 
                             validators=[InputRequired()])
    t_leakrate = IntegerField('Enter the leakage rate of these taps in L/min', 
                             validators=[InputRequired()])
    t_dishwash = IntegerField('Enter the time taken to wash dishes in min', 
                             validators=[InputRequired()])
    s_rwh = IntegerField('Enter the water saved using RWH im m^3', 
                             validators=[InputRequired()])
    
    submit = SubmitField('Submit')


