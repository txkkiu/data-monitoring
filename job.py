import os

jobs = []

class Job():
    def __init__(self, name, cron_schedule, command, parse_func):
        self.name = name
        self.cron_schedule = cron_schedule
        self.command = command
        self.parse_func = parse_func
        self.q = {}
        jobs.append(self)
    
    def add(self, k, v):
        if k not in q.keys():
            q[k] = v
        else:
            q[k] = str(q[k]) + str(v) 

    def func(self, key, value):
        if isinstance(value, dict):
            for k, v in value.iteritems():
                func(str(key) + '.' + k, v)
        else:
            add(key, str(value))

    def wrapper(self, d):
        for k, v in d.iteritems():
            func(k, v)

    def flush(self):
        for k, v in q.iteritems():
            

    def run(self):
        # execute the command
        output = os.system(self.command)
        self.parse_func(output)
