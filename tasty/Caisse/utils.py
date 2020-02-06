import os
import pandas as pd
import numpy as np
import secrets
import os
from PIL import Image
from wtforms.fields.html5 import DateField
import datetime
from datetime import timedelta
from flask import current_app, url_for
from flask_mail import Message
from datetime import datetime
import pymongo
from pymongo import MongoClient
#from sshtunnel import SSHTunnelForwarder
import pandas as pd
import ast


#Lardon56!
#mongodb+srv://<username>:<password>@lelardon-gpgol.mongodb.net/test?retryWrites=true&w=majority

def Get_MongoDB():
    '''
        Connect to mongo machine on port 27017 and get LeLardon
    '''
    # Connection Parameters
    Params = "mongodb+srv://lardon:140889@lelardon-gpgol.mongodb.net/test?retryWrites=true&w=majority"
    #Params = "mongodb+srv://lardon:Lardon56!@lelardon-gpgol.mongodb.net/test?retryWrites=true"
    # GET DB via pymongo
    client = pymongo.MongoClient(Params)
    db = client['Lardon']
    return db

def load_DB_collection(db_mongo,collection):
    cursor = db_mongo[collection].find()
    df =  pd.DataFrame(list(cursor))
    if len(df)>0:
        df = df.drop(['_id'], axis=1)
    return df

def Open_Tic(db_mongo):
    mycollection = db_mongo[ "Ticket_ID" ]
    now = datetime.now()
    date_time = now.strftime("%m%d%Y-%H%M%S")
    mycollection.insert_one({"ID" : date_time,"Paiment":"NonDef","Closed":False})

def Close_Tic(db_mongo,ID):
    mycollection = db_mongo[ "Ticket_ID" ]
    mycollection.find_one_and_update(filter={'ID':ID}, update={"$set": {'Closed': True }})

def Close_Tic_mod(db_mongo,ID,mod):
    mycollection = db_mongo[ "Ticket_ID" ]
    mycollection.find_one_and_update(filter={'ID':ID}, update={"$set": {'Paiment': mod }})


def Add_Tic(db_mongo,prod,Tic_ID,tva,price):
    mycollection = db_mongo[ "Ticket" ]
    df =  pd.DataFrame(list(mycollection.find()))
    ID = prod+Tic_ID
    # On regarde si la collection n'est pas vide
    if len(df)>0:
        df =  df[df['Tic_ID']==Tic_ID]
        # On regarde si il reste des elements apres le filtre sur Tic_ID
        if len(df)>0:
            if prod in list(df['produit']):
                # Si le produit a deja ete rentre on lui met +1
                mycollection.find_one_and_update(filter={'prod_ID':ID}, update={"$set": {'Qte': mycollection.find_one({'prod_ID':ID})['Qte'] + 1 }})
            else:
                #Sinon on le cree
                mycollection.insert_one({"produit" : prod,'TVA' : tva , 'Prix': price, "Tic_ID":Tic_ID, 'Qte':1, 'prod_ID':prod+Tic_ID})
        else:
            #Sinon on le cree
            mycollection.insert_one({"produit" : prod,'TVA' : tva , 'Prix': price,"Tic_ID":Tic_ID, 'Qte':1, 'prod_ID':prod+Tic_ID})
    else:
        #Sinon on le cree
        mycollection.insert_one({"produit" : prod,'TVA' : tva , 'Prix': price,"Tic_ID":Tic_ID, 'Qte':1, 'prod_ID':prod+Tic_ID})

def Remove_onefrom_Tic(db_mongo,prod,Tic_ID):
    mycollection = db_mongo[ "Ticket" ]
    ID = prod+Tic_ID
    mycollection.find_one_and_update(filter={'prod_ID':ID}, update={"$set": {'Qte': mycollection.find_one({'prod_ID':ID})['Qte'] - 1 }})
