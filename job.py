import os
import history_tracker

jobs = []

class Job():
    def __init__(self, name, command, parse_func):
        self.name = name
        self.command = command
        self.parse_func = parse_func
        self.q = {}
        jobs.append(self)
    
    def add_to_q(self, k, v):
        if k not in self.q.keys():
            self.q[k] = v
        else:
            self.q[k] = str(self.q[k]) + str(v) 

    def traverse_helper(self, key, value):
        if isinstance(value, dict):
            for k, v in value.iteritems():
                self.traverse_helper(str(key) + '.' + k, v)
        else:
            self.add_to_q(key, str(value))

    def traverse(self, d):
        for k, v in d.iteritems():
            self.traverse_helper(k, v)

    def flush_q(self):
        keys = self.q.keys()
        while len(self.q) != 0:
            k, v = self.q.popitem()
            history_tracker.set_pair(k, v, self.name)
        return keys

    def run(self):
        # execute the command
        output = os.system(self.command)
        d = self.parse_func(output)
        self.traverse(d)
        print(history_tracker.track_deletes(self.name, self.flush_q()))