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
    
    def add_to_q(self, k, v):
        if k not in q.keys():
            q[k] = v
        else:
            q[k] = str(q[k]) + str(v) 

    def traverse_helper(self, key, value):
        if isinstance(value, dict):
            for k, v in value.iteritems():
                traverse_helper(str(key) + '.' + k, v)
        else:
            add_to_q(key, str(value))

    def traverse(self, d):
        for k, v in d.iteritems():
            traverse_helper(k, v)

    def flush_q(self):
        while len(q) != 0:
            k, v = popitem()
            # TODO add this to history

    def run(self):
        # execute the command
        output = os.system(self.command)
        d = self.parse_func(output)
        traverse(d)
        flush_q()
    
    def schedule_job(self):
        
