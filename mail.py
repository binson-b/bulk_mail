import smtplib, dns.resolver
from email.mime.text import MIMEText
import time
import sys
from datetime import datetime
from mako.template import Template


# import sqlite3
# conn = sqlite3.connect('col_list.db')
# c = conn.cursor()
# results = c.execute("select * from kerala_colleges")
# print results.fetchone()
# conn.commit()
# conn.close()
# print dir(results)

'''
['gmail.com', 'ammini.edu.in', 'aryanet.org', 'awhengg.org', 'btcc.ac.in', 'bccaarmel.ac.in', 'yahoo.com', 'christknowledgecity.com', 'eranadknowledgecity.com', 'fisat.ac.in', 'hcet.in', 'yahoo.in', 'HOLYKINGSCOLLEGE.COM', 'iesce.info', 'icet.ac.in', 'igmt.org', 'jaibharathengg.com', 'rediffmail.com', 'jcmcsiit.ac.in', 'jecc.ac.in', 'kmeacollege.ac.in', 'KRGCE.IN', 'kmpce.org', 'meaec.edu.in', 'anjarakandy.in', 'mangalam.in', 'mbcpeermade.com', 'mbcet.org', 'MBITS.EDU.IN', 'marian.ac.in', 'mesitam.ac.in', 'mcetonline.com', 'mookambika.ac.in', 'musaliarcollege.com', 'musaliarcollegeckl.in', 'macev.org', 'muthootgroup.com', 'nmitkerala.ac.in', 'paacet.com', 'pinnacle.ac.in', 'providencecollege.org', 'riet.edu.in', 'royalcet.ac.in', 'saintgits.org', 'sist.in', 'scmsgroup.org', 'snmimt.edu.in', 'sbce.ac.in', 'bsnl.in', 'sngist.org', 'sngce.ac.in', 'snit.edu.in', 'sjcetpalai.ac.in', 'stcet.net', 'stisttvm.edu.in', 'tkmit.ac.in', 'tistcochin.edu.in', 'toms.ac.in', 'universalcollege.net', 'vedavyasa.org', 'vidyaacademy.ac.in', 'vidyatcklmr.ac.in', 'visat.ac.in', 'vjec.ac.in', 'vjcet.org', 'ycet.ac.in', 'yit.ac.in', 'fossee.in']
'''


def email_send(to, subject, msg):
    try:
        mail_from = "certificates@fossee.in"
        message = MIMEText(msg, 'html')
        message['Subject'] = subject
        message['From'] = mail_from
        message['to'] = to
        message['reply-to'] = 'certificates@fossee.in'
        message['return-to'] = 'certificates@fossee.in'
        smtpObj.sendmail(mail_from, to, message.as_string())
        return "Successfully sent"
    except smtplib.SMTPException, e:
        print '############', e
        return "Error:unable to send email"

log = open('mail.log', 'a')
log.write('\n\n############ {0} ############\n\n'.format(datetime.now()))
bounce_emails = open('mail-bounce.csv','a')
username = "P17153" 
password = 'binson@123'
smtpObj = smtplib.SMTP(host='smtp-auth.iitb.ac.in', port=25)
# smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587) # doesnot work with iitb net
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.ehlo()
smtpObj.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
smtpObj.login(username, password)
domain_list = ['gmail.com']



try:
    file_name = sys.argv[1]
    email_file = open(file_name, 'r')
    names_emails = email_file.readlines()
    subject = 'Python Workshop Certificate, FOSSEE'
    for line in  names_emails:
        msg_to_send = open('/home/binson/workspace/Mail/html_templates/certificate_mail.html', 'r')
        # fname, lname,  email = line.split(',')
        fname, email = line.split(',')
        email = email.strip('\n')
        templ = Template(msg_to_send.read()).render(fname=fname)
        email_domain = email[email.find('@')+1:]
        if email_domain in domain_list:
            message = email_send(email, subject, templ)
            print '>>>>>', fname
        else:
            try:
                mx_hosts = dns.resolver.query(email_domain, 'MX')
                if mx_hosts:
                    message = email_send(email, subject, templ)
                    print '>>>>>', fname
                domain_list.append(email_domain)
            except dns.resolver.NoAnswer:
                message = 'no email'
                bounce_emails.write('\n\n{0},{1}'.format(fname,email))
                log.write('{0}\t{1}\t{2}\n'.format(email.strip(), message, datetime.now()))
                e = 'The DNS response does not contain an answer to the question: IN MX'
                log.write('{0}\n'.format(e))    
                log.write('####################################################\n\n') 
                continue
        msg_to_send.close()
        log.write('{0}\t{1}\t{2}\n'.format(email.strip(), message, datetime.now()))
        log.write('{0}\n'.format(msg_to_send))
        log.write('####################################################\n\n')
        time.sleep(5)
    smtpObj.quit()
    email_file.close()
    print domain_list
    bounce_emails.close()
except IndexError:
    e = 'pass a single file argument after the python file'
    log.write('{0}\n'.format(e))
    print e
except IOError:
    e = 'No such file: '+file_name
    log.write('{0}\n'.format(e))
    print e
log.close()
