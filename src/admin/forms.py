from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired('* Username required.')])
	password = PasswordField('password', validators=[InputRequired('* Password required.')])
