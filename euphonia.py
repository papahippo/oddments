#!/usr/bin/python3
"""
This is really a branch of music_mailer.py.... and would be handled as such if I were
just a bt more competent and conident with git!
"""
import sys, os, re
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
from email.message import EmailMessage
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
        import subscribers
    except ImportError:
        print("Can't import subscribers module; did you forget to copy 'subscribers.py' to '%s'"
              "\n or are you in not in the per-mailing directory?" % cwd)
        sys.exist(990)
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
            print("I found nothing to attach so will not send mail at all to %s" %email_addr)
            continue
        if not email_addr:
            print ("We have no email address for %s."  % name)
            print ("perhaps you need to print the above would-be attachments?")
            continue
        # Create the message
        msg = EmailMessage()
        subject = subscribers.title.format(**locals())
        print('mail subject will be "%s"' % subject)
        msg['Subject'] = subject
        msg['To'] = email_addr
        msg['From'] = 'hippos@chello.nl'
        # msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        file_list = ",\n".join(['  %s' %filename for filename in files_to_attach])
        msg.set_content(subscribers.salutation.format(**locals()) + "\n\n"
            + subscribers.pre_text +"\n\n"
            + file_list + "\n\n"
            + subscribers.sign_off  + "\n\n"
            + subscribers.post_text + "\n\n"
                        )
        # Add the html version.  This converts the message into a multipart/alternative
        # container, with the original text message as the first part and the new html
        # message as the second part.
        icon_cid = make_msgid()
        msg.add_alternative(str(
            h.html | ("\n",
                h.head | (
                ),
                h.body | (
                    h.p | subscribers.salutation.format(**locals()),
                    h.p | subscribers.pre_text,
                    h.p | ([(name, h.br) for name in files_to_attach]),
                    h.p | (h.img(src="cid:%s" % icon_cid[1:-1]), subscribers.sign_off),
                    h.p | (h.em | (h.small |subscribers.post_text)),
                      )
            )
        ), subtype='html')
        # note that we needed to peel the <> off the msgid for use in the html.

        # Now add the related image to the html part.
        with open(subscribers.sign_off_icon, 'rb') as img:
            msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                             cid=icon_cid)
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
        if command in ('q', 'quit'):
            sys.exit(0)
        if command in ('s', 'send'): # 'send' in sys.argv:
            with smtplib.SMTP('smtp.upcmail.nl') as s:
                s.send_message(msg)
                print ("mail has been sent to '%s'." % email_addr)

if __name__ == '__main__':
    main()
