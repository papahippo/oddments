#!/usr/bin/python3

import sys, os, re, time, smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

# For guessing MIME type based on file name extension
import mimetypes
import email.utils
from email.header import Header

from phileas import _html40 as h

MagicMailTreeName = 'MagicMailTree'

# SMTP_server = 'smtp.upcmail.nl'
# SMTP_server = 'smtp.gmail.com'
SMTP_server = 'smtp.kpnmail.nl'

# ok_exts = ('.pdf', '.jpg', '.jpeg')

def gather(list_of_name_tuples, upper_dir):
    for simple_name in os.listdir(upper_dir):
        longer_name = upper_dir + os.sep + simple_name
        if os.path.isdir(longer_name):
            gather(list_of_name_tuples, longer_name)
        else:
            list_of_name_tuples.append((simple_name, longer_name))


def main():
    script_filename = sys.argv.pop(0)
    script_shortname = os.path.split(script_filename)[1]
    ok_commands = ('take', 'check', 'send', 'quit')
    command = (sys.argv and sys.argv.pop(0)) or 'check'
    if command not in ok_commands:
        print("error: %s is not one of %s." %(command, ok_commands))
        sys.exit(999)
    cwd = os.getcwd()
    path_elements = cwd.split(os.sep)
    mailing_id = path_elements.pop()
    if path_elements.pop() != MagicMailTreeName:
        print("error: %s is not within a '%s' directory." %(mailing_id, MagicMailTreeName))
        sys.exit(997)

    if command not in ('take',):
        dir_to_take_from = None
    else:
        if not sys.argv:
            print("error: take requires directory argument.")
            sys.exit(998)
        dir_to_take_from = sys.argv.pop()
        files_to_take = []
        gather(files_to_take, dir_to_take_from)
        print('\n'.join([str(t) for t in files_to_take]))

    try:
        sys.path.insert(0, '')
        import subscribers
        sys.path.pop(0)
    except ImportError:
        print("Can't import subscribers module; did you forget to copy 'subscribers.py' to '%s'"
              "\n or are you in not in the per-mailing directory?" % cwd)
        sys.exit(990)
    # identify all possible attachments once only, before checking per-user.
    #
    # now look at each potential recipient in turn:
    #
    for name, email_addr, instrument_re in subscribers.what_goes_to_whom:
        try:
            files_to_attach = os.listdir(name)
        except FileNotFoundError:
            print ("warning: no subdirectory for instrument group '%s' " % name)
            files_to_attach = None

        if dir_to_take_from:
# command 'take'
            if files_to_attach is None:
                print("creating subdirectory for instrument group '%s' " % name)
                os.mkdir(name)
            if files_to_attach:
                print("%u files/links are already present for instrument group '%s': %s"
                       % ( len(files_to_attach), name, files_to_attach))
            instrument_cre = re.compile(instrument_re)
            for simple_name, longer_name in files_to_take:
                if not instrument_cre.search(simple_name.lower()):
                    continue
                print("putting symbolic link  to '%s' in subdirectory '%s'"
                          % (simple_name, name))
                try:
                    os.symlink(longer_name,
                           name + os.sep + simple_name)
                except FileExistsError:
                    print ("warning: '%s' already exists in '%s' and will NOT be overwritten!"
                           %(simple_name, name))
            continue # that's all for take command!
# command 'check' or 'send'
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
        print('    mail will appear to come from "%s<%s>"' % (subscribers.sender_name, subscribers.sender_address))
        print('    mail recipient(s) will be "%s"' % email_addr)
        print('    mail attachment(s) will be ...\n%s' % file_list)
        message_id_string = None
        msg['From'] = email.utils.formataddr((str(Header(subscribers.sender_name, 'utf-8')), subscribers.sender_address))
        msg['Reply-to'] = email.utils.formataddr((str(Header(subscribers.reply_to_name, 'utf-8')), subscribers.reply_to_address))
        msg['Subject'] = subject
        msg['To'] = email_addr
        utc_from_epoch = time.time()
        msg['Date'] = email.utils.formatdate(utc_from_epoch, localtime=True)
        msg['Messsage-Id'] = email.utils.make_msgid(message_id_string)
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        textual_part = MIMEMultipart('alternative')
# prepare the plain version of the message body
        plain_layout = (subscribers.salutation + "\n\n"
            + subscribers.pre_text +"\n\n"
            + file_list + "\n\n"
            + subscribers.sign_off  + "\n\n"
            + subscribers.post_text + "\n\n"
                  )
# prepare the HTML version of the message body
# note that we need to peel the <> off the msgid for use in the html.
        icon_content_id = email.utils.make_msgid()
        html_layout = get_html_layout()
        str(
            h.html | ("\n",
                h.head | (
                ),
                h.body | (
                    h.p | subscribers.salutation,
                    h.p | subscribers.pre_text,
                    h.p | (h.small | ([(name, h.br) for name in files_to_attach])),
                    h.p | getattr(subscribers, "mid_text", ''),
                    h.p | (h.img(src="cid:%s" % icon_content_id[1:-1]), subscribers.sign_off),
                    h.p | (h.em | (h.small |subscribers.post_text)),
                      )
            )
        )
        print ("<<<", html_layout, ">>>")
        # Prepare both parts and insert them into the message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        for layout, subtype in (
                (plain_layout, 'plain'),
                (html_layout,  'html'),
        ):
            text = layout.format(**locals())
            sub_part =  MIMEText(text, subtype)
            textual_part.attach(sub_part)

        related_part = MIMEMultipart('related')
        related_part.attach(textual_part)

        with open(subscribers.sign_off_icon, 'rb') as img:
            img_data = img.read()
        image_part = MIMEImage(img_data)
        image_part.add_header('Content-Id', icon_content_id)
        related_part.attach(image_part)

        msg.attach(related_part)

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
            with smtplib.SMTP(subscribers.SMTP_server) as s:
                s.send_message(msg)
                print ("mail has been sent to '%s'." % email_addr)

if __name__ == '__main__':
    main()
