from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional, Email

class Register(FlaskForm):
    """register form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20, message="20 characters maximum")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])