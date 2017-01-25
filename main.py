from pymongo import MongoClient
import sendgrid
import os
from sendgrid.helpers.mail import *
import datetime
import getpass
import cmd
import pandas
import pymongo
'''
authors: Koushik Krishnan, Nick Kalteux
'''
# Config
sendgrid_key = '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'
source_email = 'krishnan.koushik@gmail.com'
dest_email = 'krishnan.koushik@gmail.com'

client = MongoClient()
db = client.primer
sg = sendgrid.SendGridAPIClient(apikey=sendgrid_key)
rows, columns = os.popen('stty size', 'r').read().split()
pandas.set_option('display.width', int(columns))
# COMMNANDS
# SET KEY, VALUE 
# GET KEY 
# DROP KEY 

def send_email(t_type, history):
    from_email = Email(source_email)
    to_email = Email(dest_email)
    subject = 'DATA_ADDED' if t_type == 'CREATE' else 'DATA_UPDATED'
    body = 'User ' + history['user'] + ' has ' + t_type + 'D key = ' + history['key'] + ' with value = ' + history['value']
    content = Content('text/plain', body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code


def set_pair(key, value):
    data_in = {}
    data_in[str(key)] = str(value)
    data_in['id'] = str(key)
    t_type = 'CREATE'
    success = False
    if db.data.find_one({'id':str(key)}) is not None:
        post = db.data.find_one({'id':str(key)})
        post[key] = value
        post['id'] = key
        db.data.save(post)
        t_type = 'UPDATE'
        success = True
    else:
        success = db.data.insert_one(data_in).acknowledged
    if success:
        now = datetime.datetime.now()
        key_data = str(key)
        value_data = str(value)
        user = getpass.getuser()
        history_in = {}

        history_in['key'] = key_data
        history_in['value'] = value_data
        history_in['user'] = user
        history_in['type'] = t_type
        history_in['timestamp'] = now
        result_h = db.history.insert_one(history_in)
        send_email(t_type, history_in)
        return 'success'

def history(num_rows=-1):
    history = []
    if num_rows < 0:
        for x in db.history.find().sort('timestamp',pymongo.DESCENDING):
            history += [x]
    else:
        for x in db.history.find().sort('timestamp',pymongo.DESCENDING).limit(num_rows):
            history += [x]        

    df = pandas.DataFrame(history)
    df = df[['timestamp', 'type', 'user', 'key', 'value']]
    return df

    

def get_value(key):
    if db.data.find_one({'id': key}) is not None:
        return db.data.find_one({'id': key})[key]
    else:
        return 'key not found'

    
class KeyValueStore(cmd.Cmd):
    
    def do_set(self, line):
        '''set [key], [value]
        if the key exists, the value will be updated
        otherwise a new key value pair will be created
        '''
        if len(line.split(',')) < 2:
            print('Error set takes 2 arguments "KEY, VALUE"')
        else:
            key, value = line.split(',')[0], line.split(',')[1]
            print(set_pair(key, value))

    def do_get(self, line):
        '''get [key]
        if the key exists, the value will be returned
        otherwise you will be notified that the key is absent
        '''
        if len(line.split()) != 1:
            print('Error get takes 2 arguments "KEY"')
        else:
            print(get_value(line))

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

    def do_EOF(self, line):
        '''halt current stream of input
        '''
        return True
    
if __name__ == '__main__':
    KeyValueStore().cmdloop()
            
