from history_tracker import *


keys = ['_id','key','user','type','timestamp','value','old_value']

#functions dealing with importance and alerting
def match_rule(rule, history_in):
    for key in rule:
        if re.match(str(rule[key]), str(history_in[key])):
            return True
    return False

def is_important(history_in):
    for rule in rules:
        current_rule = dict.fromkeys(keys, r'\b\B')

        # populate the current_rule
        for regex_tuple in rule['regexes']:
            current_rule[regex_tuple[0]] = regex_tuple[1]
        # check if the current rule matches this history instance 
        return match_rule(current_rule, history_in)

def send_email(t_type, history, source_email, dest_email):
    #TODO: Implement this to work on Filoseta's machine
    msg = MIMEMultipart()
    msg['From'] = source_email
    msg['To'] = dest_email
    subject = 'DATA_ADDED' if t_type == 'CREATE' else 'DATA_UPDATED'
    msg['Subject'] = subject
    body = 'User ' + history['user'] + ' has ' + t_type + 'D key = ' + history['key'] + ' with value = ' + history['value']
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('')
    s.sendmail(source_email, [dest_email], msg.as_string())
    s.quit()