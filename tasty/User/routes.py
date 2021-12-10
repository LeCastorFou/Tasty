from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import db, bcrypt, mail
from tasty.models import User

from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from tasty.User.forms import RegistrationForm, LoginForm
from tasty.Caisse.utils import Get_MongoDB, Add_Tic, Remove_prodfrom_Tic, load_DB_collection, Open_Tic, Remove_onefrom_Tic, Close_Tic, Close_Tic_mod
import pandas as pd
import secrets
import os
from datetime import timedelta
import math
import json
from flask import jsonify
import datetime
import numpy as np

userbp = Blueprint('userbp',__name__)

db_mongo = Get_MongoDB()

@userbp.route("/register", methods=['GET','POST'])
#@login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # sucess is a bootsrap class
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash("Compte créé !", 'success')
        return redirect(url_for('usersbp.Login'))
    return render_template('User/register.html', form=form)

@userbp.route("/Login",methods=['GET','POST'])
#@login_required
def Login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        form = LoginForm()
        return render_template('User/Login.html', form = form)


@userbp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('mainbp.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Un email vous a été envoyé !', 'info')
        return redirect(url_for('usersbp.Login'))
    return render_template('reset_request.html', title='Reset Password', form=form)
