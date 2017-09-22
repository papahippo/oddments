#!/usr/bin/python3
"""
wanted someting like this to send mail to my GSM when home isdn line is called...
... I've written off ISDN as obsolescent and am now using this script as a basis for
an automated sheet music mailer: see musicmailer.py.
"""
import sys, os, re
from importlib import util
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid

sys.path.insert(0, '')
from phileas import _html40 as h

def main():
    recipient_patterns = []
    script_filename = sys.argv.pop(0)
    fixed_answer = subscribers = None
    while sys.argv:
        arg = sys.argv.pop(0)
        if arg.startswith('-'):
            fixed_answer = arg[1:].lower()
            if fixed_answer in ('y', 'yes', 'n', 'no', 'q', 'quit'):
                continue
            print("syntax: music_mailer [-y|-n] [pattern...]\n ('%s' is not allowed!)" % fixed_answer)
            sys.exit(990)
        recipient_patterns.append(arg)
    path_elements = os.getcwd().split(os.sep)
    # print (path_elements)
    music_title = possible_title = ''
    module_name = 'subscribers'
    while path_elements:
        if not subscribers:
            ancestral_path = os.sep.join(path_elements)
            # print (ancestral_path)
            spec = util.spec_from_file_location(module_name,
                                                ancestral_path + os.sep + module_name + '.py')
            # print (spec)
            if spec:
                subscribers = util.module_from_spec(spec)
                if subscribers:
                    try:
                        spec.loader.exec_module(subscribers)
                        print("'%s' taken from directory \"%s\"." % (module_name, ancestral_path))
                    except FileNotFoundError:
                        subscribers = None
        pe = path_elements.pop()
        if not music_title and len(pe) == 1:
            music_title = possible_title.replace('_', ' ')
        possible_title = pe
        if subscribers:
            continue
    ok_exts = ('.pdf', '.jpg', '.jpeg')
    only_files = [f for f in os.listdir('.') if (os.path.isfile(f)
                                    and os.path.splitext(f)[1].lower() in ok_exts)]
    for name, email_addr, instrument_re in subscribers.what_goes_to_whom:
        if recipient_patterns:
            for rp in recipient_patterns:
                if re.search(rp, name):
                    break
            else:
                continue
        if not email_addr:
            print ("Skipping '%s', for whom we have no email address." % name)
            continue
        files_to_attach = []
        print ("looking which music to send to %s (based on regular expression '%s'...)"
                 %(name, instrument_re))
        first_name = name.split(' ')[0]
        instrument_cre = re.compile(instrument_re)
        for candidate in only_files:
            cl = candidate.lower()
            if instrument_cre.search(candidate.lower()):
                print ("  %s" % candidate)
                files_to_attach.append(candidate)
        if not files_to_attach:
            print("I found nothing to attach so will not send mail at all to %s" %email_addr)
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
            + subscribers.post_text + "\n\n"
            + subscribers.sign_off  + "\n"
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
                    h.p | "Hello",
                    h.p | "Is this looking some bit like?",
                    h.img(src="cid:%s" % icon_cid[1:-1]),
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
        answer = fixed_answer or input("send this mail (yes, no or quit )?").strip()
        if answer in ('q', 'quit'):
            sys.exit(0)
        if answer in ('y', 'yes'): # 'send' in sys.argv:
            with smtplib.SMTP('smtp.upcmail.nl') as s:
                s.send_message(msg)
                print ("mail has been sent to '%s'." % email_addr)

if __name__ == '__main__':
    main()
