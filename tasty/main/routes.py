from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import bcrypt, mail
#from tasty.models import User, Post
from werkzeug import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import pandas as pd
import secrets
import os
from datetime import timedelta
import math
from PIL import Image
import plotly
import json
from flask import jsonify
import datetime
######### LOADING BDD ########
#exec(open(os.getcwd() + '/tasty/MongoConnection/Functions_Mongo.py').read())
#exec(open('MongoConnection/Functions_Mongo.py').read())

### Acces to the DB ####
#db_mongo  = Get_MongoDB()
#ColNames = db_mongo.collection_names()
#ColNames.sort()

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/coworking")
def coworking():
    return render_template('coworking.html')

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/reservation")
def reservation():
    return render_template('reservation.html')

@main.route("/cours")
def cours():
    return render_template('cours.html')

@main.route("/cafe")
def cafe():
    return render_template('cafe.html')

@main.route("/contact")
def contact():
    return render_template('contact.html')
