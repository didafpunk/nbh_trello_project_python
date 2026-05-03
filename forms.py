from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class ProfileForm(FlaskForm):
    fullname = StringField('Nom complet', validators=[DataRequired(), Length(min=3)])
    mail = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Mettre à jour')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmer', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Changer le mot de passe')
    
    
class LoginForm(FlaskForm):
    mail = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')    
    
class SignupForm(FlaskForm):
    mail = StringField('Email', validators=[DataRequired(), Email()])
    fullname = StringField('Nom complet', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("S'inscrire")    