from history_tracker import *
#for formatting in terminal
rows, columns = os.popen('stty size', 'r').read().split()
pandas.set_option('display.width', int(columns))


#command line wrappers for functions in history tracker    
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
    
    def do_histuser(self, line):
        '''histuser [user]
        retrieve history of changes made by specified user
        '''
        user = line.split(' ')[0]
        l = get_user(user)
        if(len(l) > 0):
            print(pandas.DataFrame(l)[['timestamp', 'type', 'user', 'key', 'value', 'old_value']])
        else:
            print "no keys found for user: ", user 
    
    def do_histkey(self,line):
        '''histkey [key]
        retrieve history of changes made to specified key
        '''
        key = line.split(' ')[0]
        l = get_key(key)
        if(len(l) > 0):
            print(pandas.DataFrame(l)[['timestamp', 'type', 'user', 'key', 'value', 'old_value']])
        else:
            print "no keys found for key: ", key 
    
    def do_histregex(self, line):
        '''histkey [key]
        retrieve history of changes made to keys matching regex pattern
        '''
        regex = line
        l = get_important(regex)
        if(len(l) > 0):
            print(pandas.DataFrame(l)[['timestamp', 'type', 'user', 'key', 'value', 'old_value']])
        else:
            print "no keys found for regex: ", regex 

    def do_EOF(self, line):
        '''halt current stream of input
        '''
        return True
    
if __name__ == '__main__':
    KeyValueStore().cmdloop()
            
