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

# global variables
test = True
smtp_host = 'localhost'
smtp_port = 25
if test:
    smtp_host = 'smtp-auth.iitb.ac.in'


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
	#print smtpObj.noop()[0]
	global smtpObj
	smtp_conn = is_connected(smtpObj)
	if not smtp_conn:
	    smtpObj = connectSMTP()
	    smtp_conn = True
    	if smtp_conn:
            smtpObj.sendmail("bounce-mail@fossee.in", to, message.as_string()) # TOADDR+CCADDR to send to cc ids
	    logger_s.info('Sucessfully Sent to  %s', to)
            return True
    except smtplib.SMTPException, e:
	logger_e.debug('%s', e)
	return False

def connectSMTP():
    smtpObj = smtplib.SMTP(host=smtp_host, port=smtp_port)
    smtpObj.ehlo()
    smtpObj.starttls()
    if test:
	smtpObj.ehlo()
	smtpObj.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
	from local_settings import username, password
	smtpObj.login(username, password)
    return smtpObj

def is_connected(conn):
    try:
        status = conn.noop()[0]
    except smtplib.SMTPServerDisconnected:
        status = -1
    return True if status == 250 else False


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
    #  0: 'certificates@fossee.in'                      #
    #  1: 'workshops@fossee.in'                         #
    #  2: 'coodinator-certificate'                      #
    #  3: 'scipy@fossee.in',				#
    #  4: 'Scipy India 2017                             #
    #  9: 'test@fossee.in'                              #
    #                                                   #
    #####################################################
    
    """

    i = input("Please select the desired Mail-box : ")
    # if you change the key of certificate in mail_box (0:'certificates@fossee.in') then change 'not i'to 'i == changed_key'
    if not i:
	while True:
	    workshop_code = raw_input("Please select the Workshop Name (i-ISCP, b-BPPy): ")
	    if workshop_code == 'i' or workshop_code == 'b':
		break
	    else:
		continue
    # to use the same template and send to both types of workshop
    workshop_name = {
		     'i': 'Introduction to Scientific Computing using Python',
		     'b': 'Basic Programming using Python',
    }
    mail_box = {
                0: 'certificates@fossee.in',
                1: 'workshops@fossee.in',
                3: 'scipy@fossee.in',
                9: 'test@fossee.in',
    }
    mail_box.update({2: mail_box[0], 4: mail_box[0]})
    subject = {
                0: 'Python Workshop Certificate, FOSSEE',
                1: 'Remote-assisted Python Workshop by FOSSEE, IIT Bombay',
                3: 'SciPy 2017 invitation',
		4: 'SciPy India 2017 Certificate, Fossee',
                9: 'TEST'
    }
    subject.update({2: subject[0]})
    print 'mail-box: %s\nsubject: %s' % (mail_box[i], subject[i])
    template_loc = {
                    0: os.path.abspath('html_templates/certificate_mail.html'),
                    1: os.path.abspath('html_templates/python_workshop_invite_2017-0.html'),
                    2: os.path.abspath('html_templates/coordinator_certificate.html'),
                    3: os.path.abspath('html_templates/scipy_conference_2017_invite_email.html'),
		    4: os.path.abspath('html_templates/scipy_participant_certificate_2017.html'),
                    9: os.path.abspath('html_templates/test.html')
    }
    for j, line in  enumerate(names_emails):
        msg_to_send = open(template_loc[i], 'r')
        #fname, email = line.split(',') # only use when name is there in csv
        fname = ''
	if i:
	    workshop_code = 'i'
        email = line.strip()
	email = email.strip('\n')
	templ = Template(msg_to_send.read()).render(fname=fname, workshop_name=workshop_name[workshop_code])
	message = email_send(email, subject[i], templ, files)
	time.sleep(20)
        msg_to_send.close()
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
