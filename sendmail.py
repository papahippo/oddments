#!/usr/bin/python3
"""
want someting like this to send mail to my GSM when home isdn line is called
"""
import sys
import smtplib
from email.mime.text import MIMEText

def sendmail(sender='gill@luna.myerscough.nl',
             recipients=['hippos@chello.nl',],
             subject='mail sent from python script',
             content='(no real mesage content)',
             smtp = 'smtp.upcmail.nl'):
    if not isinstance(recipients, (list, tuple)):
        recipients = recipients.split(',')
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    s = smtplib.SMTP(smtp)
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

def main():
    sendmail(**dict([key_eq_val.split('=') for key_eq_val in sys.argv[1:]]))
if __name__ == '__main__':
    main()
