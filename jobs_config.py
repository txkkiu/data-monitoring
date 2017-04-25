from job import Job
# create a new job

def ldap_parse_func(input):
    

ldap_kkrishnan8 = Job(name='kkrishnan8_test', 
                        cron_scedule='* * * * *', 
                        command='ldapsearch -H ldap://gtad01.ad.gatech.edu -b DC=ad,DC=gatech,DC=edu samaccountname=kkrishnan8')