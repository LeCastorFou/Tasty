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

caisse = Blueprint('caisse',__name__)

db_mongo = Get_MongoDB()

@caisse.route("/Caisse_Carte")
#@login_required
def Caisse_Carte():
    Ticket_ID = load_DB_collection(db_mongo,'Ticket_ID')
    # Si il y a des tickets en BDD et si il sont tous fermé on redirige vers la creation de ticket
    if len(Ticket_ID) !=0:
        if not all([e for e in list(Ticket_ID["Closed"])]):
            Ticket_ID_En_Cours  = list(Ticket_ID[Ticket_ID['Closed'] == False]['ID'])[0]
            print("Ticket en cours")
            print(Ticket_ID_En_Cours)
            boissons = Boisson.query.all()
            foods = Food.query.all()
            produits = Product.query.all()
            All_Tickets = load_DB_collection(db_mongo,'Ticket')
            if len(All_Tickets)>0:
                All_Tickets['Prix'] = [float(e) for e in list(All_Tickets['Prix'])]
                All_Tickets = All_Tickets[All_Tickets['Tic_ID'] == Ticket_ID_En_Cours]
            All_Tickets = All_Tickets.to_dict('index')
            return render_template('Caisse/Caisse_Carte.html',boissons=boissons,foods = foods,All_Tickets=All_Tickets,produits=produits,Ticket_ID_En_Cours=Ticket_ID_En_Cours)
        else:
            return redirect(url_for('caisse.Caisse_Carte_init'))
    else:
        return redirect(url_for('caisse.Caisse_Carte_init'))

@caisse.route("/Caisse_Carte_init")
#@login_required
def Caisse_Carte_init():
    All_Daily_sum = load_DB_collection(db_mongo,'Daily_summary')
    if len(All_Daily_sum) >0:
        Dates = np.sort(np.unique(All_Daily_sum['Date']))[::-1]
        Dates = Dates[0:3]
        list_df = []
        for e in Dates:
            list_df = list_df+[All_Daily_sum[All_Daily_sum['Date']==e].reset_index()]
        list_df = list_df[0]
        list_df = list_df.drop(['index','Date'],axis =1)
        list_df = list_df[['Summary','Prix_tot']]
        list_df['Prix_tot'] = [round(e,2) for e in list_df['Prix_tot']]
        return render_template('Caisse/Caisse_Carte_init.html', tables=[list_df.to_html(classes='steelBlueCols')],titles=list_df.columns.values, date = pd.to_datetime(Dates[0]).strftime("%m/%d/%Y") )
    else:
        return render_template('Caisse/Caisse_Carte_init.html', tables=[],titles=[], date = '' )
# Open ticket when none is open
@caisse.route('/Open_ticket',methods = ['POST'])
#@login_required
def Open_ticket():
    # On créé un nouveau ticket OPEN
    Open_Tic(db_mongo)
    return redirect(url_for('caisse.Caisse_Carte'))

# Closing ticket
@caisse.route('/close_ticket/<string:Tic_ID>',methods = ['POST'])
#@login_required
def close_ticket(Tic_ID):
    # On ferme le ticket
    print(Tic_ID)
    Close_Tic(db_mongo,Tic_ID)
    return jsonify(matching_results=['res'])

# Closing ticket
@caisse.route('/close_caisse',methods = ['Get'])
#@login_required
def close_caisse():
    today = datetime.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    All_Daily_sum = load_DB_collection(db_mongo,'Daily_summary')
    if len(All_Daily_sum)>0:
        if today in list(All_Daily_sum['Date']):
            flash('La caisse a déjà été fermé', 'error')
            return redirect(url_for('caisse.Caisse_Carte_init'))

    Ticket_ID = load_DB_collection(db_mongo,'Ticket_ID')
    Ticket_ID = Ticket_ID.rename(columns={'ID': 'Tic_ID'})
    All_Tickets = load_DB_collection(db_mongo,'Ticket')
    Daily_summary = pd.merge(Ticket_ID,All_Tickets, on="Tic_ID")
    Daily_summary['Prix'] = [float(e) for e in list(Daily_summary['Prix'])]
    Daily_summary['Prix_tot'] = Daily_summary['Prix']*Daily_summary['Qte']
    Daily_summary['Date'] = [ datetime.datetime.strptime(e[:8],'%m%d%Y') for e in Daily_summary['Tic_ID'] ]
    Daily_summary = Daily_summary[Daily_summary['Date'] == today]
    Total = np.sum(Daily_summary['Prix_tot'])
    TVA_ventil = pd.DataFrame(Daily_summary.groupby(['TVA'])['Prix_tot'].sum())
    Paiement_ventil = pd.DataFrame(Daily_summary.groupby(['Paiment'])['Prix_tot'].sum())
    Produit_ventil = pd.DataFrame(Daily_summary.groupby(['produit'])['Prix_tot'].sum())
    Summary = pd.concat([Produit_ventil, TVA_ventil,Paiement_ventil], ignore_index=False)
    Summary['Summary'] = Summary.index
    Summary = Summary.append({'Prix_tot': np.sum(list(Daily_summary['Qte'])),'Summary':'Nombre de vente'}, ignore_index=True)
    Summary = Summary.append({'Prix_tot': len(np.unique(Daily_summary['Tic_ID'])),'Summary':'Nombre de Ticket'}, ignore_index=True)
    panier_moyen =np.mean(pd.DataFrame(Daily_summary.groupby(['Tic_ID'])['Prix_tot'].sum())['Prix_tot'])
    Summary = Summary.append({'Prix_tot': panier_moyen,'Summary':'panier moyen'}, ignore_index=True)
    Summary = Summary.append({'Prix_tot': Total,'Summary':'Total'}, ignore_index=True)
    Summary['Date'] = today
    # Saving
    Summary = Summary.to_dict('records')
    db_mongo["Daily_summary"].insert_many(Summary)
    return redirect(url_for('caisse.Caisse_Carte_init'))


# Closing ticket mode de Paiement
@caisse.route('/close_ticket_mod/<string:Tic_ID>/<string:mod>',methods = ['POST'])
#@login_required
def close_ticket_mod(Tic_ID,mod):
    # On ecrit le moyen de Paiement
    Close_Tic_mod(db_mongo,Tic_ID,mod)
    return jsonify(matching_results=['res'])


# Save action with jquery fction without reloading DataFrame
@caisse.route('/Add_to_ticket/<string:prod>/<string:Tic_ID>/<string:tva>/<string:price>/<string:qte>',methods = ['POST'])
#@login_required
def Add_to_ticket(prod,Tic_ID,tva,price,qte):
    # On ajoute prod au ticket dans la bdd mongo
    Add_Tic(db_mongo,prod,Tic_ID,tva,price,qte)
    All_Tickets = load_DB_collection(db_mongo,'Ticket')
    All_Tickets = All_Tickets[All_Tickets['Tic_ID']==Tic_ID]
    total = np.sum([float(list(All_Tickets['Prix'])[i])*float(list(All_Tickets['Qte'])[i]) for i in range(len(All_Tickets))])
    All_Tickets = All_Tickets[All_Tickets['produit']==prod]

    res = list(All_Tickets['Qte'])[0]
    return jsonify(matching_results=[str(res),str(total)])


@caisse.route('/remove_to_ticket/<string:prod>/<string:Tic_ID>',methods = ['POST'])
#@login_required
def remove_to_ticket(prod,Tic_ID):
    # On enleve prod au ticket dans la bdd mongo
    Remove_onefrom_Tic(db_mongo,prod,Tic_ID)
    All_Tickets = load_DB_collection(db_mongo,'Ticket')
    All_Tickets = All_Tickets[All_Tickets['Tic_ID']==Tic_ID]
    total = np.sum([float(list(All_Tickets['Prix'])[i])*float(list(All_Tickets['Qte'])[i]) for i in range(len(All_Tickets))])
    All_Tickets = All_Tickets[All_Tickets['produit']==prod]
    res = list(All_Tickets['Qte'])[0]
    return jsonify(matching_results=[str(res),str(total)])

@caisse.route('/remove_prod_to_ticket/<string:prod>/<string:Tic_ID>',methods = ['POST'])
#@login_required
def remove_prod_to_ticket(prod,Tic_ID):
    # On enleve prod au ticket dans la bdd mongo
    Remove_prodfrom_Tic(db_mongo,prod,Tic_ID)
    All_Tickets = load_DB_collection(db_mongo,'Ticket')
    All_Tickets = All_Tickets[All_Tickets['Tic_ID']==Tic_ID]
    total = np.sum([float(list(All_Tickets['Prix'])[i])*float(list(All_Tickets['Qte'])[i]) for i in range(len(All_Tickets))])
    All_Tickets = All_Tickets[All_Tickets['produit']==prod]
    res = list(All_Tickets['Qte'])
    if len(res) >0:
        res =res[0]
    else:
        res = 0
    return jsonify(matching_results=[str(res),str(total)])
