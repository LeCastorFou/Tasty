from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import db, bcrypt, mail
from tasty.models import User, Post,Product, Boisson, Food
from werkzeug import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
#from tasty.Caisse.forms importForms ...
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

API = Blueprint('API',__name__)

db_mongo = Get_MongoDB()

@API.route('/test', methods=['GET'])
def test():
    return jsonify(['test'])

@API.route('/weightproj/<string:IMC>/<string:pre_week>/<string:wei>', methods=['GET'])
def weightproj(IMC,pre_week,wei):
    IMC = float(IMC)
    pre_week = float(pre_week)
    wei = float(wei)
    week_vec = np.linspace(0,40,41)
    all_max = []
    all_min = []
    all_meam = []

    if IMC < 18.5:
        for e in week_vec:
            if e < 13:
                max_w = round(2/13*e,2)
                min_w = round(0.5/13*e,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
            else:
                max_w = round(16/27*e-5.7,2)
                min_w = round(12/27*e-5.2,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
    elif IMC > 18.5 and IMC <25:
        for e in week_vec:
            if e < 13:
                max_w = round(2/13*e,2)
                min_w = round(0.5/13*e,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
            else:
                max_w = round(14/27*e-4.7,2)
                min_w = round(11/27*e-4.8,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
    elif IMC > 25 and IMC <30:
        for e in week_vec:
            if e < 13:
                max_w = round(2/13*e,2)
                min_w = round(0.5/13*e,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
            else:
                max_w = round(9.5/27*e-2.57,2)
                min_w = round(6.5/27*e-2.63,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
    elif IMC >30:
        for e in week_vec:
            if e < 13:
                max_w = round(2/13*e,2)
                min_w = round(0.5/13*e,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]
            else:
                max_w = round(7/27*e-1.33,2)
                min_w = round(4.5/27*e-1.66,2)
                mean_w = round(np.mean([max_w,min_w]),2)
                all_max  = all_max + [max_w]
                all_min  = all_min + [min_w]
                all_meam  = all_meam + [mean_w]

    my_res = pd.DataFrame.from_dict({'week':week_vec,'P_min':all_min,'P_max':all_max,'Pmean':all_meam})
    my_res = my_res.to_dict('record')

    return jsonify(my_res)
