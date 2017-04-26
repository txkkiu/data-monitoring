
#Rules configuration is done here
#rules is a list of dicts pairing regexes with emails
#regexes are tuples of history column to matching regexes
#emails are a list of emails to be alerted on when these regexes are triggered
#TODO: write logic to send to list of emails
rules = [
    {
        'regexes': [('key', 'important'), ('value', 'important')],
        'emails': ['kalteuxn@gmail.com', 'kkrishnan8@gatech.edu']
    }
]