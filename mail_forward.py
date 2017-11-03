import smtplib, imaplib, email

imap_host = "imap.iitb.ac.in"
smtp_host = "smtp-auth.iitb.ac.in"
smtp_port = 25
user = "p17153"
passwd = "binson@123"
msgid = "7:10"
from_addr = "bnsn.babu@gmail.com"
to_addr = "bnsn.babu@gmail.com"

# open IMAP connection and fetch message with id msgid
# store message data in email_data
client = imaplib.IMAP4(imap_host)
client.login(user, passwd)
client.select('INBOX')
#status, data = client.fetch(msgid, "(RFC822)")
typ, msgnums = client.search(None, '(From "cash@iitb.ac.in")')
#email_data = data[0][1]
client.close()
client.logout()
print typ, msgnums
# create a Message instance from the email data
message = email.message_from_string(email_data)
exit()
# replace headers (could do other processing here)
message.replace_header("From", from_addr)
message.replace_header("To", to_addr)
message.replace_header('Cc', ' ')
# open authenticated SMTP connection and send message with
# specified envelope from and to addresses
smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
smtp.login(user, passwd)
smtp.sendmail(from_addr, to_addr, message.as_string())
smtp.quit()
