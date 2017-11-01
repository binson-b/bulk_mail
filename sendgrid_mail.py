# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
import sys
from sendgrid.helpers.mail import *

file_name = sys.argv[1]
email_file = open(file_name, 'r')
names_emails = email_file.readlines()

for lines in names_emails:
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	email_content = open('/home/binson/workspace/Mail/html_templates/scipy_conference_2017_invite_email.html','r').read()
	from_email = Email("scipy@fossee.in")
	to_email = Email(lines)
	subject = 'SciPy 2017 invitation'
	content = Content("text/html", email_content)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)
