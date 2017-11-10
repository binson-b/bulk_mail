import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application  import MIMEApplication
import time
import sys
from datetime import datetime
import os
from mako.template import Template
from os.path import basename
import logging


test = False

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def setup_logger(log_file, name, level=logging.DEBUG):
    """Function setup as many loggers as you want""" 

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def email_send(to, subject, msg, files=None):
    try:
        mail_from = mail_box[i]
        message = MIMEMultipart()
	message['Subject'] = subject
        message['From'] = mail_from
        message['To'] = to
        message['reply-to'] = mail_box[i]
	# message['Cc'] = ''
        message.attach(MIMEText(msg, 'html'))
        # Attachment code
	for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                    )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            message.attach(part)
        smtpObj.sendmail("bounce-mail@fossee.in", to, message.as_string()) # TOADDR+CCADDR to send to cc ids
	logger_s.info('Sucessfully Sent to  %s', to)
        return True
    except smtplib.SMTPException, e:
	logger_e.debug('%s', e)
	return False

def connectSMTP():
    smtpObj = smtplib.SMTP(host='localhost', port=25)
    smtpObj.ehlo()
    smtpObj.starttls()
    if test:
	smtpObj = smtplib.SMTP(host='smtp-auth.iitb.ac.in', port=25)
	smtpObj.ehlo()
	smtpObj.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
	import local_setting
	smtpObj.login(username, password)
    return smtpObj
logger_s = setup_logger('mail_success.log', name='Success')
logger_e = setup_logger('mail_error.log', name='Error')

try:
    file_name = sys.argv[1]
    files = sys.argv[2:] or []
    email_file = open(file_name, 'r')
    names_emails = email_file.readlines()
    smtpObj=connectSMTP()
    print """
    #####################################################
    #                                                   #
    #  0:'certificates@fossee.in'                       #
    #  1:'workshops@fossee.in'                          #
    #  2:'coodinator-certificate'                       #
    #  3:'scipy@fossee.in',                             #
    #  9:'test@fossee.in'                               #
    #                                                   #
    #####################################################
    
    Note: It will send to scipy@fossee.in 
    """

    i = 3 # input("Please select the desired Mail-box : ")

    mail_box = {
                0:'certificates@fossee.in',
                1:'workshops@fossee.in',
                3:'scipy@fossee.in',
                9:'test@fossee.in',
    }
    mail_box.update({2: mail_box[0],})
    subject = {
                0:'Python Workshop Certificate, FOSSEE',
                1:'Remote-assisted Python Workshop by FOSSEE, IIT Bombay',
                3: 'SciPy 2017 invitation',
                9: 'TEST'
    }
    subject.update({2: subject[0]})
    print 'mail-box: %s\nsubject: %s' % (mail_box[i], subject[i])
    template_loc = {
                    0:os.path.abspath('html_templates/certificate_mail.html'),
                    1:os.path.abspath('html_templates/python_workshop_invite_2017-0.html'),
                    2:os.path.abspath('html_templates/coordinator_certificate.html'),
                    3:os.path.abspath('html_templates/scipy_conference_2017_invite_email.html'),
                    9:os.path.abspath('html_templates/test.html')
    }
    for j, line in  enumerate(names_emails):
        msg_to_send = open(template_loc[i], 'r')
        # fname, email = line.split(',') # only use when name is there in csv
        fname = ''
        email = line.strip()
        email = email.strip('\n')
        templ = Template(msg_to_send.read()).render(fname=fname)
	message = email_send(email, subject[i], templ, files)
        msg_to_send.close()
        time.sleep(30)
    smtpObj.quit()
    email_file.close()
    if not file_name == 'demo.csv':
        os.rename(file_name,file_name[:-4]+'-completed.csv')
except IndexError:
    e = 'pass a single file argument after the python file'
    logger_e.debug('%s', e)
    raise Exception(e)
except IOError:
    e = 'No such file: '+file_name
    logger_e.debug('%s', e)
    raise Exception(e)
