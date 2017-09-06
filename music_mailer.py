#!/usr/bin/python3
"""
wanted someting like this to send mail to my GSM when home isdn line is called...
... I've written off ISDN as obsolescent and am now using this script as a basis for
an automated sheet music mailer: see musicmailer.py.
"""
import sys, re
from os import listdir
from os.path import isfile, join, splitext

from email.mime.text import MIMEText
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
from email.message import EmailMessage
from email.policy import SMTP
sys.path.insert(0, '')
import what_to_whom


def main():
    ok_exts = ('.pdf', '.jpg', '.jpeg')
    only_files = [f for f in listdir('.') if (isfile(f)
                                    and splitext(f)[1].lower() in ok_exts)]
    files_to_attach = []
    for email_addr, telltaletexts in what_to_whom.sections:
        print ("looking which music to send to %s ..." %email_addr)
        telltale_cres = [re.compile(ttt) for ttt in telltaletexts]
        for candidate in only_files:
            cl = candidate.lower()
            for cre in telltale_cres:
                if cre.search(cl):
                    print (candidate)
                    files_to_attach.append(candidate)
                    break
        if not files_to_attach:
            print("I found nothing to attach so will not send mail at all to %s" %email_addr)
            break
        # Create the message
        msg = EmailMessage()
        msg['Subject'] = "MEW bladmuziek (script test!)" # % os.path.abspath(directory)
        msg['To'] = email_addr
        msg['From'] = 'hippos@chello.nl'
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        msg.set_content("[this will be a quasi-personallized message in the final product]")

        for filename in files_to_attach:
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(filename, 'rb') as fp:
                msg.add_attachment(fp.read(),
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=filename)
        if 'send' in sys.argv:
            with smtplib.SMTP('smtp.upcmail.nl') as s:
                s.send_message(msg)


if __name__ == '__main__':
    main()
