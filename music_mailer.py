#!/usr/bin/python3

import sys, os, re
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

# For guessing MIME type based on file name extension
import mimetypes
from email.utils import make_msgid

from phileas import _html40 as h

def main():
    script_filename = sys.argv.pop(0)
    script_shortname = os.path.split(script_filename)[1]
    ok_commands = ('check', 'send', 'quit')
    command = (sys.argv and sys.argv.pop(0)) or 'check'
    if command not in ok_commands:
        print("error: %s is not one of %s." %(command, ok_commands))
        sys.exit(990)
    cwd = os.getcwd()
    path_elements = cwd.split(os.sep)
    mailing_id = path_elements.pop()
    try:
        sys.path.insert(0, '')
        import subscribers
        sys.path.pop(0)
    except ImportError:
        print("Can't import subscribers module; did you forget to copy 'subscribers.py' to '%s'"
              "\n or are you in not in the per-mailing directory?" % cwd)
        sys.exit(990)
    # identify all possible attachments once only, before chacking per-user.
    #
    ok_exts = ('.pdf', '.jpg', '.jpeg')
    # now look at each potential recipient in turn:
    #
    for name, email_addr, instrument_re in subscribers.what_goes_to_whom:
        try:
            files_to_attach = os.listdir(name)
        except FileNotFoundError:
            print ("warning: no subdirectory for instrument group '%s' " % name)
            files_to_attach = None
        if not files_to_attach:
            # message below can get in the way, so maybe suppress it?:
            print("I found nothing to attach so will not send mail at all to '%s'" % name)
            continue
        if not email_addr:
            print ("We have no email address for %s."  % name)
            print ("perhaps you need to print the above would-be attachments?")
            continue
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        subject = subscribers.title.format(**locals())
        files_to_attach.sort()
        file_list = ",\n".join(['      %s' %filename for filename in files_to_attach])
        print('preparing mail for intrument (group) "%s"' % name)
        print('    mail subject will be "%s"' % subject)
        print('    mail recipient(s) will be "%s"' % email_addr)
        print('    mail attachment(s) will be ...\n%s' % file_list)
        msg['Subject'] = subject
        msg['To'] = email_addr
        msg['From'] = 'hippos@chello.nl'
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

# prepare the plain version of the message body
        if 0:
            plain_layout = (subscribers.salutation + "\n\n"
                + subscribers.pre_text +"\n\n"
                + file_list + "\n\n"
                + subscribers.sign_off  + "\n\n"
                + subscribers.post_text + "\n\n"
                      )
        else:
            plain_layout = ("[HMTL email hieronder en/of attachments niet leesbaar?"
                            " neem dan meteen contact op met verzender!]")
# prepare the HTML version of the message body
# note that we need to peel the <> off the msgid for use in the html.
        icon_content_id = make_msgid()
        html_layout = str(
            h.html | ("\n",
                h.head | (
                ),
                h.body | (
                    h.p | subscribers.salutation,
                    h.p | subscribers.pre_text,
                    h.p | ([(name, h.br) for name in files_to_attach]),
                    h.p | (h.img(src="cid:%s" % icon_content_id[1:-1]), subscribers.sign_off),
                    h.p | (h.em | (h.small |subscribers.post_text)),
                      )
            )
        )
        # Prepare both parts and insert them into the message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        for layout, subtype in (
                (plain_layout, 'plain'),
                (html_layout,  'html'),
        ):
            text = layout.format(**locals())
            part =  MIMEText(text, subtype)
            msg.attach(part)

        # Now add the related image to the html part.
        with open(subscribers.sign_off_icon, 'rb') as img:
            img_data = img.read()
        part = MIMEImage(img_data)
        part.add_header('Content-Id', icon_content_id)
        msg.attach(part)

        for filename in files_to_attach:
            rel_name = os.path.join(name, filename)
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(rel_name)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(rel_name, 'rb') as attachment:
                attachment_data = attachment.read()
            part = MIMEBase(maintype, subtype)
            part.set_payload(attachment_data)
            # Encode the payload using Base64
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(rel_name))
            msg.attach(part)
        print ("length of message is %u bytes" % len(bytes(msg)))
        if command in ('q', 'quit'):
            sys.exit(0)
        if command in ('s', 'send',): # 'send' in sys.argv:
            with smtplib.SMTP('smtp.upcmail.nl') as s:
                s.send_message(msg)
                print ("mail has been sent to '%s'." % email_addr)

if __name__ == '__main__':
    main()
