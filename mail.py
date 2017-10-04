import smtplib, dns.resolver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application  import MIMEApplication
import time
import sys
from datetime import datetime
import os
from mako.template import Template
from domain_list import domain_list
from local_settings import username, password
from os.path import basename


# import sqlite3
# conn = sqlite3.connect('col_list.db')
# c = conn.cursor()
# results = c.execute("select * from kerala_colleges")
# print results.fetchone()
# conn.commit()
# conn.close()
# print dir(results)

def email_send(to, subject, msg, files=None):
    try:
        mail_from = mail_box[i]
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = mail_from
        message['to'] = to
        #message['cc'] = mail_from
        message['reply-to'] = mail_box[i]
        message['return-path'] = "bounce-mail@fossee.in" #'certificates@fossee.in'
        message.attach(MIMEText(msg, 'html'))
        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                    )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            message.attach(part)
        smtpObj.sendmail(mail_from, to, message.as_string())
        return "Successfully sent"
    except smtplib.SMTPException, e:
        print '############', e
        return "Error:unable to send email"

log = open('mail.log', 'a')
log.write('\n\n############ {0} ############\n\n'.format(datetime.now()))
bounce_emails = open('mail-bounce.csv','a')
smtpObj = smtplib.SMTP(host='smtp-auth.iitb.ac.in', port=25)
# smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587) # doesnot work with iitb net
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.ehlo()
smtpObj.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
smtpObj.login(username, password)

print """
#####################################################
#                                                   #
#  0:'certificates@fossee.in'                       #
#  1:'workshops@fossee.in'                          #
#  2:'coodinator-certificate'                       #
#  3:'test@fossee.in'                               #
#                                                   #
#####################################################

"""

i = input("Please select the desired Mail-box : ")


try:
    file_name = sys.argv[1]
    files = sys.argv[2:] or []
    email_file = open(file_name, 'r')
    names_emails = email_file.readlines()
    mail_box = {
                0:'certificates@fossee.in',
                1:'workshops@fossee.in',
                3:'test@fossee.in'
    }
    mail_box.update({2: mail_box[0],})
    subject = {
                0:'Python Workshop Certificate, FOSSEE',
                1:'Remote-assisted Python Workshop by FOSSEE, IIT Bombay',
                3: 'TEST'
    }
    subject.update({2: subject[0]})
    print 'mail-box: %s\nsubject: %s' % (mail_box[i], subject[i])
    template_loc = {
                    0:os.path.abspath('html_templates/certificate_mail.html'),
                    1:os.path.abspath('html_templates/python_workshop_invite_2017-0.html'),
                    2:os.path.abspath('html_templates/coordinator_certificate.html'),
                    3:os.path.abspath('html_templates/test.html')
    }
    for line in  names_emails:
        msg_to_send = open(template_loc[i], 'r')
        # fname, email = line.split(',') # only use when name is there in csv
        fname = ''
        email = line.strip()
        email = email.strip('\n')
        templ = Template(msg_to_send.read()).render(fname=fname)
        email_domain = email[email.find('@')+1:]
        if email_domain in domain_list:
            message = email_send(email, subject[i], templ, files)
            print '>>>>>', fname if fname else email
        else:
            try:
                mx_hosts = dns.resolver.query(email_domain, 'MX')
                if mx_hosts:
                    message = email_send(email, subject, templ, files)
                    print '>>>>>', fname if fname else email
                domain_list.append(email_domain)
            except (dns.resolver.NoAnswer ,dns.exception.Timeout,dns.resolver.NXDOMAIN):
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
    if not file_name == 'demo.csv':
        os.rename(file_name,file_name[:-4]+'-completed.csv')
except IndexError:
    e = 'pass a single file argument after the python file'
    log.write('{0}\n'.format(e))
    print e
except IOError:
    e = 'No such file: '+file_name
    log.write('{0}\n'.format(e))
    print e
log.close()
