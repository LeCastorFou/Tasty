from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import StringField, SelectField, PasswordField, SelectMultipleField, FloatField, SubmitField, BooleanField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from tasty.models import User, Post,Product
from flask_uploads import UploadSet, IMAGES
from flask_login import current_user
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
import datetime
#Wtform permet de faire toute les validations
# taille, no empty, email pour que l'input de l'utilisateur soit ok
images = UploadSet('images', IMAGES)

class AddPost(FlaskForm):
    title = StringField('Nom', validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    details = TextAreaField('Date/Details', validators=[DataRequired()])
    picture = FileField('Image :', validators=[])
    #picture = FileField('Image :', validators=[])
    submit = SubmitField('Ajouter')
