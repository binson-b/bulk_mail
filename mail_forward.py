import smtplib, imaplib, email
from datetime import datetime
import logging


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
#user = ""
#passwd = ""
#msgid = "7"
from_addr = "zxz@gmail.com"
to_addr = "zbc@gmail.com"

# open IMAP connection and fetch message with id msgid
# store message data in email_data
client = imaplib.IMAP4(imap_host)
client.login(user, passwd)
client.select('INBOX')
typ, msgnums = client.search(None, 'ALL')
smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.ehlo()
smtp.starttls()
#smtp.ehlo()
#smtp.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
#smtp.login(user, passwd)
now = datetime.now()
for i in msgnums[0].split():
    status, data = client.fetch(i, "(RFC822)")
    email_data = data[0][1]
    # create a Message instance from the email data
    message = email.message_from_string(email_data)
    if 'Date' in message:
	message_date = message['Date'].split()
	message_date = ' '.join(message_date[:5])
	try:
	    date = datetime.strptime(message_date, '%a, %d %b %Y %H:%M:%S')
	except ValueError:
	    logger_e.debug("Error: %s, %s" %(i, message_date))
	date_diff = now-date
	if date_diff.days <= 30:
	    # replace headers (could do other processing here)
	    message.replace_header("From", from_addr)
	    message.replace_header("To", to_addr)
	    if 'Cc' in message:
		message.replace_header('Cc', ' ')
	    # open authenticated SMTP connection and send message with
	    # specified envelope from and to addresses
	    # from_addr arg is the return-path address
	    smtp.sendmail(from_addr, to_addr, message.as_string()) 
	    logger_s.info('id: %s to_email: %s email_date: %s' %(i, to_addr, message_date))
smtp.quit()
client.close()
client.logout()

