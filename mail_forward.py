import smtplib, imaplib, email
from datetime import datetime
import logging
import time

test = True

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

# loggers
logger_s = setup_logger('mail_forward_success.log', name='Success')
logger_e = setup_logger('mail_forward_error.log', name='Error')

# Client host and port
imap_host = "imap.iitb.ac.in"
smtp_host = "smtp-auth.iitb.ac.in"
smtp_port = 25
user = ""
passwd = ""
#msgid = "7"
from_addr = ""
to_addr = ["example1@gmail.com", "emaple2@gmail.com"]

# open IMAP connection and fetch message with id msgid
# store message data in email_data
client = imaplib.IMAP4(imap_host)
if (user and passwd) == '' and test:
    from local_settings import username, password
    user = username
    passwd = password
client.login(user, passwd)
client.select('INBOX')
# client.search(None, 'ALL') # search for all mails
# client.search(None, '(Subject, "keyword")') # search for keyword in subject of all mails
typ, msgnums = client.search(None, '(Text "salary")') # search for keyword in sub + body of all mails

def create_conn():
    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.ehlo()
    smtp.starttls()
    if test:
	smtp.ehlo()
	smtp.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
	from local_settings import username, password
	smtp.login(username, password)
    return smtp

def is_connected(conn):
    try:
        status = conn.noop()[0]
    except smtplib.SMTPServerDisconnected:
        status = -1
    return True if status == 250 else False

smtp = create_conn()
for i in msgnums[0].split():
    # client.fetch(i, "BODY[Header]") # only fetch header
    status, data = client.fetch(i, "(RFC822)") # fetches body+Header
    email_data = data[0][1]
    # create a Message instance from the email data
    message = email.message_from_string(email_data)
    if test:
	pass
        #print message
        #continue
	
    if 'Date' in message:
	message_date = message['Date'].split()
	message_date_s = ' '.join(message_date[:5])
	try:
	    date = datetime.strptime(message_date_s, '%a, %d %b %Y %H:%M:%S')
	except ValueError:
	    message_date_s = ' '.join(message_date[:4])
	    try:
	        date = datetime.strptime(message_date_s, '%d %b %Y %H:%M:%S') 
	    except ValueError:
	        logger_e.debug("Error: %s, %s" %(i, message_date_s))
	if date.month >= 10 and date.year==2017:
	    # replace headers (could do other processing here)
	    message.replace_header("From", from_addr)
	    message.replace_header("To", ','.join(to_addr))
	    if 'Cc' in message:
		message.replace_header('Cc', ' ')
	    # open authenticated SMTP connection and send message with
	    # specified envelope from and to addresses
	    # from_addr arg is the return-path address
	    smtp_conn = is_connected(smtp)
	    if not smtp_conn:
	        smtp = create_conn()
		smtp_conn = True
	    if smtp_conn:
		time.sleep(20)
		smtp.sendmail(from_addr, to_addr, message.as_string())
		logger_s.info('id: %s to_email: %s email_date: %s' %(i, to_addr, message_date_s))
	    #break
smtp.quit()
client.close()
client.logout()
