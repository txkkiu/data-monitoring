import history_tracker

data = {}

n = 30
db_name = 'new_db'

for i in range(n):
    data["k" + str(i)] = "v" + str(i)

for k, v in data.iteritems():
    history_tracker.set_pair(k, v, db_name)

print(history_tracker.history())

for k, v in data.iteritems():
    assert history_tracker.server_get_value(k, db_name) != 'key not found'

for k, v in data.iteritems():
    history_tracker.delete_key(k, db_name)
    assert history_tracker.server_get_value(k, db_name) == ''

print(history_tracker.history())