from pymongo import MongoClient
import smtplib
import os
import datetime
import getpass
import cmd
import pandas
import pymongo
import time
import requests
import json
import ast
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rules import rules
import re
import sendgrid
from sendgrid.helpers.mail import *
from email_config import *
import email_config
from importance import *

client = MongoClient()
db = client.primer
#sets a key-value pair in rocks and records the transaction in mongo
def set_pair(key, value, rocksdb):
    data_in = {}
    data_in[str(key)] = str(value)
    data_in['id'] = str(key)
    t_type = 'CREATE'
    success = False
    history_in = {}
    oldValue = server_get_value(key, rocksdb)
    if oldValue == value:
        return "new value identical to current value"
    if oldValue is not "key not found" and oldValue != "":
        history_in['old_value'] = oldValue
        t_type = 'UPDATE'
        success = server_set_value(key, value, rocksdb)
    else:
        success = server_set_value(key, value, rocksdb)
        history_in['old_value'] = ""
    if success:
        now = datetime.datetime.now()
        key_data = str(key)
        value_data = str(value)
        user = getpass.getuser()
        
        history_in['key'] = key_data
        history_in['value'] = value_data
        history_in['user'] = user
        history_in['type'] = t_type
        history_in['timestamp'] = now
        db.history.insert_one(history_in)

        if is_important(history_in):
            #send_email_sendgrid(t_type, history_in)
            print "important key detected"
        return 'success'
#functions that wrap around mongo queries
def get_value(key):
    if db.data.find_one({'id': key}) is not None:
        return db.data.find_one({'id': key})[key]
    else:
        return 'key not found'

def get_user(user):
    return list(db.history.find({'user':user}))

def get_key(key):
    return list(db.history.find({'key':key}))

def get_important(regex):
    return list(db.history.find({'key': {'$regex': regex}}))

def history(num_rows=-1):
    history = []
    if num_rows < 0:
        for x in db.history.find().sort('timestamp',pymongo.DESCENDING):
            history += [x]
    else:
        for x in db.history.find().sort('timestamp',pymongo.DESCENDING).limit(num_rows):
            history += [x]
    df = pandas.DataFrame(history)
    df = df[['timestamp', 'type', 'user', 'key', 'value', 'old_value']]
    return df

#Functions dealing with key-value store, rocksdb
#rocks needs to be running for these to work
def server_get_value(key , rocksdb):
    url = "http://localhost:8080/get"
    querystring = {"key":key, "db": rocksdb}
    response = requests.request("GET", url, params=querystring)
    if response.status_code != requests.codes.ok:
        return "key not found" 
    return json.loads(response.text)['value']  

def server_set_value(key, value, rocksdb):
    url = "http://localhost:8080/set"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"value\"\r\n\r\n" + value + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"key\"\r\n\r\n"+ key + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"db\"\r\n\r\n" + rocksdb +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"      
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.status_code == requests.codes.ok

#compares the previous database instance with the current database, after a job runs
#deletes all missing keys, storing information about these deletes in the history database     
def track_deletes(db, keys):
    url = "http://localhost:8080/keys?db=db" 
    querystring = {"db": db}
    response = requests.request("GET", url, params=querystring)
    if response.status_code != requests.codes.ok:
        return "key not found" 
    #figure out what to do with this
    oldkeys = json.loads(response.text)[] 
    deletedkeys = list(set(oldkeys) - set(keys))
    for deletedkey in deletedkeys:
        t_type = "DELETE"
        history_in = {}
        oldValue = server_get_value(oldValue)
        history_in['old_value'] = oldValue
        now = datetime.datetime.now()
        key_data = str(deletedkey)
        user = getpass.getuser()
        history_in['key'] = key_data
        history_in['value'] = ""
        history_in['user'] = user
        history_in['type'] = t_type
        history_in['timestamp'] = now
        db.history.insert_one(history_in)
        delete_key(deletedkey, db)

def delete_key(key, db):
    url = "http://localhost:8080/delete"
    querystring = {"key":key, "db": rocksdb}
    response = requests.request("POST", url, params=querystring)
    if response.status_code != requests.codes.ok:
        return "key not found" 
    return json.loads(response.text)['value']      
def get_value(key):
    if db.data.find_one({'id': key}) is not None:
        return db.data.find_one({'id': key})[key]
    else:
        return 'key not found'

def get_user(user):
    return list(db.history.find({'user':user}))
def get_key(key):
    return list(db.history.find({'key':key}))
def get_important(regex):
    return list(db.history.find({'key': {'$regex': regex}}))
