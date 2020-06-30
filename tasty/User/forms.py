from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, SelectMultipleField, SubmitField, BooleanField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from tasty.models import User
from flask_login import current_user
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
import datetime
#Wtform permet de faire toute les validations
# taille, no empty, email pour que l'input de l'utilisateur soit ok


def user_query():
    return Team.query

def get_pk(obj):
    return str(obj)

def get_current_user():
    return current_user

class RegistrationForm(FlaskForm):
    username = StringField("Pseudo ('prenom-nom' de préférence)",validators=[DataRequired(),Length(min =2, max = 20)])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Mot de passe perso', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe perso',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("S'inscrire")

    # ajouter une error custom pour eviter les doublons dans la base
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("L'utilisateur existe déjà")
    # ajouter une error custom pour eviter les doublons dans la base
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("L'email est déjà pris")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    # cookie pour se rappeler du password
    remember = BooleanField('Se rappeler de moi')
    submit = SubmitField('Se connecter')

'''
class UpdateAccountForm(FlaskForm):
    username = StringField("Nom d'utilisateur",validators=[DataRequired(),Length(min =2, max = 20)])
    prenom = StringField("Prénom",validators=[DataRequired()])
    nom = StringField("Nom",validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    telephone = StringField('Téléphone',validators=[Length(max=10)])
    poid = IntegerField('Poids en kg', validators=[NumberRange(min=0, max=200)])
    taille = IntegerField('Taille en cm', validators=[NumberRange(min=0, max=250)])
    team = QuerySelectField('Equipe', query_factory=user_query, allow_blank=False, get_label='name',get_pk=get_pk)
    #En reprise (j'y vais doucement)
    healthState = SelectField('Etat de forme (En pleine forme - blessé)', choices=[('Parfait','Parfait'),('Des petits bobos','Des petits bobos'),('Moyen mais je peux faire quelques exercices','Moyen mais je peux faire quelques exercices'),("Indisponible","Indisponible"),('blessé','blessé')] , validators=[DataRequired()])
    poste_pred = IntegerField('Poste de prédilection', validators=[NumberRange(min=0, max=22)])
    details = StringField('Détail sur votre état (date de retour si blessé(e) etc ...)',validators=[Length(max=2000)])
    fonction = SelectField('Fonction au sein du club', choices=[('Joueur','Joueur'), ('Administration','Administration'),('Entraineur','Entraineur'),('supporter','supporter')], validators=[DataRequired()])
    sexe = SelectField('Sexe', choices=[('Homme','Homme'), ('Femme','Femme'),('Ne sais pas','Ne sais pas')], validators=[DataRequired()])
    picture = FileField('Photo de profil :', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Mettre à jour mon profil')

    # ajouter une error custom pour eviter les doublons dans la base
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("Le nom d'utilisateur existe déjà")

    # ajouter une error custom pour eviter les doublons dans la base
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("L'email est déjà utilisé ")
'''

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Demande de nouveau mot de passe')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Aucun compte n'est associé à cet email")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
