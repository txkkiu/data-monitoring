from job import Job
import schedule
import time

def ldap_parse_func(input):
    return {}

ldap_kkrishnan8 = Job(name='kkrishnan8_test', command='ldapsearch -H ldap://gtad01.ad.gatech.edu -b DC=ad,DC=gatech,DC=edu samaccountname=kkrishnan8', parse_func=ldap_parse_func)
schedule.every().minute.do(ldap_kkrishnan8.run)

while True:
    schedule.run_pending()
    time.sleep(1)