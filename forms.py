from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional, Email

class Register(FlaskForm):
    """register form"""

    username = StringField("username", validators=[InputRequired(), Length(min=1, max=20, message="20 characters maximum")])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    first_name = StringField("first name", validators=[InputRequired()])
    last_name = StringField("last name", validators=[InputRequired(), Email(message="Please enter a valid email")])