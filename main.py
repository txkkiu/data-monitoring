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
# Config
source_email = 'krishnan.koushik@gmail.com'
dest_email = 'kalteuxn@gmail.com'

client = MongoClient()
db = client.primer
rows, columns = os.popen('stty size', 'r').read().split()
pandas.set_option('display.width', int(columns))

def send_email(t_type, history):
    msg = MIMEMultipart()
    msg['From'] = source_email
    msg['To'] = dest_email
    subject = 'DATA_ADDED' if t_type == 'CREATE' else 'DATA_UPDATED'
    msg['Subject'] = subject
    body = 'User ' + history['user'] + ' has ' + t_type + 'D key = ' + history['key'] + ' with value = ' + history['value']
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('')
    #s.connect()
    s.sendmail(source_email, [dest_email], msg.as_string())
    s.quit()

def set_pair(key, value, rocksdb):
    data_in = {}
    data_in[str(key)] = str(value)
    data_in['id'] = str(key)
    t_type = 'CREATE'
    success = False
    history_in = {}
    oldValue = server_get_value(key, rocksdb)
    if oldValue is not "key not found":
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
        result_h = db.history.insert_one(history_in)
        #send_email(t_type, history_in)
        return 'success'

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


def get_value(key):
    if db.data.find_one({'id': key}) is not None:
        return db.data.find_one({'id': key})[key]
    else:
        return 'key not found'

    
class KeyValueStore(cmd.Cmd):
    
    def do_set(self, line):
        '''set [key], [value], [db]
        if the key exists in the specified db, the value will be updated
        otherwise a new key value pair will be created
        '''
        if len(line.split(',')) != 3:
            print('Error set takes 3 arguments "KEY, VALUE, DB"')
        else:
            key, value, rocksdb = "".join(line.split(" ")).split(',')
            print(set_pair(key, value, rocksdb))

    def do_get(self, line):
        '''get [key], [db]
        if the key exists within the specified db, the value will be returned
        otherwise you will be notified that the key is absent
        '''
        if len(line.split(',')) != 2:
            print('Error get takes 2 arguments "KEY, DB"')
        else:
            key, rocksdb = "".join(line.split(" ")).split(',')
            print(server_get_value(key, rocksdb))
    def do_hist(self, line):
        '''hist (optional) [num_rows_back]
        retrieve the last $num_rows_back$ rows in the history log
        if $num_rows_back$ is not specified, the entire history will be returned
        '''
        num_rows = -1
        try:
            num_rows = int(line.split(' ')[0])
        except ValueError:
            num_rows = -1
        
        print(history(num_rows=num_rows))
    
    def do_ihist(self, line):
        '''ihist [startDate] (optional) [endDate]
        retrieve history for specified date if one date is provided
        retrieve history for specified date range (greater than or equal to start date, less than end date) if two dates are provided
        '''
        if len(line.split(',')) < 2:
            startDate = datetime.datetime.strptime(line, "%Y-%m-%d")
            endDate = startDate + datetime.timedelta(days=1)
            print startDate
        else:
            startDate, endDate = "".join(line.split(" ")).split(',')
            startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
            endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        l = list(db.history.find({'timestamp': {'$lt': endDate , '$gte': startDate}}))
        if len(l) is 0:
            print "no transactions found within specified date range"
        else:
            print(pandas.DataFrame(l)[['timestamp', 'type', 'user', 'key', 'value', 'old_value']])
    
        
    def do_EOF(self, line):
        '''halt current stream of input
        '''
        return True
    
if __name__ == '__main__':
    KeyValueStore().cmdloop()
            
