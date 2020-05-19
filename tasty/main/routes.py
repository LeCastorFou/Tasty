from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import bcrypt, mail
from tasty.models import User, Post,Product, Boisson, Food
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import pandas as pd
from tasty.models import User, Post,Product
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
    return render_template('mainweb/index.html')

@main.route("/coworking")
def coworking():
    return render_template('mainweb/coworking.html')

@main.route("/about")
def about():
    return render_template('mainweb/about.html')

@main.route("/reservation")
def reservation():
    produits = Product.query.all()
    return render_template('mainweb/reservation.html',produits=produits)

@main.route("/cours")
def cours():
    return render_template('mainweb/cours.html')

@main.route("/cafe")
def cafe():
    boissons = Boisson.query.all()
    foods = Food.query.all()
    return render_template('mainweb/cafe.html',boissons=boissons,foods=foods)

@main.route("/contact")
def contact():
    return render_template('mainweb/contact.html')
