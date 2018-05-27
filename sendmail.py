#!/usr/bin/env python
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate, formataddr
from email import encoders
from email.header import Header

def sendMail(send_from='', send_to=[], subject='(no subject)', text='(no text)', files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(send_from, 'utf-8')), 'hippos@chello.nl'))
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__=='__main__':
    sendMail(send_from='gill@luna', send_to=['g.m.myerscough@gmail.com',],
        subject="yet another python sendMail test",
        text="perhaps attachment will be audible now!",
        files=["/home/gill/tmp/msg.mp3",]
    )
