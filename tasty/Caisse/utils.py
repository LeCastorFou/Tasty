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


def Add_Tic(db_mongo,prod,Tic_ID):
    mycollection = db_mongo[ "Ticket" ]
    df =  pd.DataFrame(list(mycollection.find()))
    ID = prod+Tic_ID
    if len(df)>0:
        if prod in list(df['produit']):
            mycollection.find_one_and_update(filter={'prod_ID':ID}, update={"$set": {'Qte': mycollection.find_one({'prod_ID':ID})['Qte'] + 1 }})
        else:
            mycollection.insert_one({"produit" : prod,"Tic_ID":Tic_ID, 'Qte':1, 'prod_ID':prod+Tic_ID})
    else:
        mycollection.insert_one({"produit" : prod,"Tic_ID":Tic_ID, 'Qte':1, 'prod_ID':prod+Tic_ID})

def Remove_onefrom_Tic(db_mongo,prod,Tic_ID):
    mycollection = db_mongo[ "Ticket" ]
    ID = prod+Tic_ID
    mycollection.find_one_and_update(filter={'prod_ID':ID}, update={"$set": {'Qte': mycollection.find_one({'prod_ID':ID})['Qte'] - 1 }})
