#!/usr/bin/python3
"""
wanted someting like this to send mail to my GSM when home isdn line is called...
... I've written off ISDN as obsolescent and am now using this script as a basis for
an automated sheet music mailer: see musicmailer.py.
"""
import sys, os, re

## from email.mime.text import MIMEText
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
from email.message import EmailMessage
from email.policy import SMTP
sys.path.insert(0, '')
from subscribers import *


def main():
    ok_exts = ('.pdf', '.jpg', '.jpeg')
    only_files = [f for f in os.listdir('.') if (os.path.isfile(f)
                                    and os.path.splitext(f)[1].lower() in ok_exts)]
    for email_addr, instrument_re in sections:
        files_to_attach = []
        print ("looking which music to send to '%s' (based on regular expression '%s'..." %(email_addr, instrument_re))
        instrument_cre = re.compile(instrument_re)
        for candidate in only_files:
            cl = candidate.lower()
            if instrument_cre.search(candidate.lower()):
                print ("  %s" %candidate)
                files_to_attach.append(candidate)
        if not files_to_attach:
            print("I found nothing to attach so will not send mail at all to %s" %email_addr)
            continue
        # Create the message
        msg = EmailMessage()
        path_elements = os.getcwd().split(os.sep)
        possible_title = ''
        while (len(possible_title) != 1) and path_elements:
            music_title = possible_title
            possible_title = path_elements.pop()
        print ("music_title=", music_title)
        msg['Subject'] = title.format(**locals())
        msg['To'] = email_addr
        msg['From'] = 'hippos@chello.nl'
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        file_list = ",\n".join(['  %s' %filename for filename in files_to_attach])
        msg.set_content(salutation.format(**locals()) + "\n\n"
            + pre_text +"\n\n"
            + file_list + "\n\n"
            + post_text + "\n\n"
            + sign_off  + "\n"
        )

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
                print ("mail has been sent to '%s'." % email_addr)
    if 'send' not in sys.argv:
        print ( "^^^^^^^^^\n"
                "if above text looks all right, send mail by entering command:\n"
                "music_mailer.py send\n")

if __name__ == '__main__':
    main()
