from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    pass

class AddPropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    num_rooms = StringField('No. of Rooms', validators=[InputRequired()])
    num_bathrooms = StringField('No. of Bathrooms', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    p_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
