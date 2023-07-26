from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from Fakepinterest.models import User

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    button_confirm = SubmitField("Login")

class FormSingUp(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField("Password Confirmation", validators=[DataRequired(), EqualTo("password")])
    button_confirm = SubmitField("Create")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            return ValidationError("This email already exist")