from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import db, bcrypt, mail
from tasty.models import User, Post,Product, Boisson, Food
from werkzeug import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from tasty.Carte.forms import AddCarteFoodForm, AddCarteBoissonForm
from tasty.Carte.utils import save_picture_carte
import pandas as pd
import secrets
import os
from datetime import timedelta
import math
import json
from flask import jsonify
import datetime
import math
######### LOADING BDD ########
#exec(open(os.getcwd() + '/tasty/MongoConnection/Functions_Mongo.py').read())
#exec(open('MongoConnection/Functions_Mongo.py').read())

### Acces to the DB ####
#db_mongo  = Get_MongoDB()
#ColNames = db_mongo.collection_names()
#ColNames.sort()

carte = Blueprint('carte',__name__)

@carte.route("/allcarte")
def allcarte():
    boissons = Boisson.query.all()
    foods = Food.query.all()
    lenboi = math.ceil(len(boissons)/4)
    lenfood= math.ceil(len(foods)/4)
    return render_template('carte/all_carte_products.html',boissons=boissons,foods = foods,lenboi=lenboi,lenfood=lenfood)

# creer une boisson :
@carte.route("/carte/add_boisson",  methods=['GET','POST'])
#@login_required
def addcarte_boisson():
    form = AddCarteBoissonForm()
    if form.validate_on_submit():
        if form.picture.data != None:
            boisson = Boisson(image_file = save_picture_carte(form.picture.data),name=form.name.data, description=form.description.data, price_sell = form.price_sell.data,TVA = form.TVA.data)
        else:
            boisson = Boisson(name=form.name.data, description=form.description.data, price_sell = form.price_sell.data,TVA = form.TVA.data)
        db.session.add(boisson)
        db.session.commit()
        flash('Boisson ajoutée','success')
        return redirect(url_for('carte.addcarte_boisson'))
    return render_template('carte/add_carte_product.html', title = 'Ajouter une boisson', form =form, legend = 'Nouvelle Boisson')

# creer une food
@carte.route("/carte/add_food",  methods=['GET','POST'])
#@login_required
def addcarte_food():
    form = AddCarteFoodForm()
    if form.validate_on_submit():
        if form.picture.data != None:
            food = Food(image_file = save_picture_carte(form.picture.data),name=form.name.data, description=form.description.data, price_sell = form.price_sell.data,TVA = form.TVA.data)
        else:
            food = Food(name=form.name.data, description=form.description.data, price_sell = form.price_sell.data,TVA = form.TVA.data)
        db.session.add(food)
        db.session.commit()
        flash('Food ajoutée','success')
        return redirect(url_for('carte.addcarte_food'))
    return render_template('carte/add_carte_product.html', title = 'Ajouter une food', form =form, legend = 'Nouvelle food')


#update prod
#@login_required
@carte.route("/food/<int:food_id>/update", methods=['GET','POST'])
def update_food(food_id):
    prod = Food.query.get_or_404(food_id)
    form = AddCarteFoodForm()
    if form.validate_on_submit():
        if form.picture.data != None:
            prod.image_file = save_picture_carte(form.picture.data)
        prod.name = form.name.data
        prod.description =form.description.data
        prod.price_sell = form.price_sell.data
        db.session.commit()
        flash('Food modifié','success')
        return redirect(url_for('carte.allcarte'))
    elif request.method == 'GET':
        form.name.data = prod.name
        form.description.data = prod.description
        form.price_sell.data = prod.price_sell
        form.picture.data = prod.image_file
    return render_template('carte/add_carte_product.html', title = 'modifier une food', form =form, legend = 'Modifier Produit')

#update prod
#@login_required
@carte.route("/boisson/<int:boisson_id>/update", methods=['GET','POST'])
def update_boisson(boisson_id):
    prod = Boisson.query.get_or_404(boisson_id)
    form = AddCarteBoissonForm()
    if form.validate_on_submit():
        if form.picture.data != None:
            prod.image_file = save_picture_carte(form.picture.data)
        prod.name = form.name.data
        prod.description =form.description.data
        prod.price_sell = form.price_sell.data
        db.session.commit()
        flash('Boisson modifié','success')
        return redirect(url_for('carte.allcarte'))
    elif request.method == 'GET':
        form.name.data = prod.name
        form.description.data = prod.description
        form.price_sell.data = prod.price_sell
        form.picture.data = prod.image_file
    return render_template('carte/add_carte_product.html', title = 'modifier une boisson', form =form, legend = 'Modifier Boisson')


# Delete prod
#@login_required
@carte.route("/food/<int:food_id>/delete", methods=['GET','POST'])
def delete_food(food_id):
    prod = Food.query.get_or_404(food_id)
    db.session.delete(prod)
    db.session.commit()
    flash('Food effacé', 'success')
    return redirect(url_for('carte.allcarte'))

# Delete prod
#@login_required
@carte.route("/boisson/<int:boisson_id>/delete", methods=['GET','POST'])
def delete_boisson(boisson_id):
    prod = Boisson.query.get_or_404(boisson_id)
    db.session.delete(prod)
    db.session.commit()
    flash('Boisson effacé', 'success')
    return redirect(url_for('carte.allcarte'))
