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
logger_e = setup_logger('mail_date_error.log', name='Error')

# Client host and port
imap_host = "imap.iitb.ac.in"
user = ""
passwd = ""

# open IMAP connection and fetch message with id msgid
# store message data in email_data
client = imaplib.IMAP4(imap_host)
client.login(user, passwd)
client.select('INBOX')
typ, msgnums = client.search(None, 'ALL')

for i in msgnums[0].split():
    status, data = client.fetch(i, "(RFC822)")
    email_data = data[0][1]
    # create a Message instance from the email data
    message = email.message_from_string(email_data)
    if 'Date' in message:
	logger_e.debug("Error: %s, %s" %(i, message['Date']))
client.close()
client.logout()
