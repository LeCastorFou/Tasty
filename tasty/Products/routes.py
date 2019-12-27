from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import db, bcrypt, mail
from tasty.models import User, Post,Product
from werkzeug import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from tasty.Products.forms import AddProductForm
from tasty.Products.utils import save_picture
import pandas as pd
import secrets
import os
from datetime import timedelta
import math
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

products = Blueprint('products',__name__)

@products.route("/allprod")
def allprod():
    produits = Product.query.all()
    return render_template('products/allproducts.html',produits=produits)

# creer un post
@products.route("/product/add",  methods=['GET','POST'])
#@login_required
def addprod():
    form = AddProductForm()
    if form.validate_on_submit():
        print(form.picture.data)
        produit = Product(image_file = save_picture(form.picture.data),name=form.name.data, description=form.description.data, price_sell = form.price_sell.data, price_buy = form.price_buy.data, qte =form.qte.data)
        print(produit)
        db.session.add(produit)
        db.session.commit()
        flash('Produit ajouté','success')
        return redirect(url_for('products.addprod'))
    return render_template('products/addproduct.html', title = 'Ajouter un produit', form =form, legend = 'Nouveau Produit')



#update prod
#@login_required
@products.route("/prod/<int:prod_id>/update", methods=['GET','POST'])
def update_post(prod_id):
    prod = Product.query.get_or_404(prod_id)
    form = AddProductForm()
    if form.validate_on_submit():
        prod.image_file = save_picture(form.picture.data)
        prod.name = form.name.data
        prod.description =form.description.data
        prod.price_sell = form.price_sell.data
        prod.price_buy = form.price_buy.data
        prod.qte = form.qte.data
        db.session.commit()
        flash('Produit modifié','success')
        return redirect(url_for('products.allprod'))
    elif request.method == 'GET':
        form.name.data = prod.name
        form.description.data = prod.description
        form.price_sell.data = prod.price_sell
        form.price_buy.data = prod.price_buy
        form.qte.data = prod.qte
        form.picture.data = prod.image_file
    return render_template('products/addproduct.html', title = 'Ajouter un produit', form =form, legend = 'Nouveau Produit')

# Delete prod
#@login_required
@products.route("/prod/<int:prod_id>/delete", methods=['GET','POST'])
def delete_post(prod_id):
    prod = Product.query.get_or_404(prod_id)
    db.session.delete(prod)
    db.session.commit()
    flash('Produit effacé', 'success')
    return redirect(url_for('products.allprod'))
