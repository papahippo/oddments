#!/usr/bin/python3
"""
music_mailer.py has a symbiotic relationship with 'subscribers.py'; either may play the role of
main script.
"""
import sys, os, re, time, smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import mimetypes
import email.utils
from email.header import Header

from phileas import _html40 as h

MagicMailTreeName = 'MagicMailTree'
# ok_exts = ('.pdf', '.jpg', '.jpeg')

def putmsg(*pp, **kw):
    print(*pp, **kw, file=sys.stderr)

class _Mailshot:
    """
    This is really a stub - but I have left some usual settings in place!
    """
    sender = 'papahippo'
    title = "[dummy title]'  voor {name}"
    salutation = "Beste muziekant,"
    pre_text = "[dummy pre-text]"
    post_text = "[dummy post-text]"
    sign_off = ("[dummy sign_off],\n\n"
    "Daddock"
    )
    sign_off_icon = "/home/gill/MEW_Archive/music_318-73071_vsmall.jpg"
    what_goes_to_whom = (
        #('tmp',  'hippos@chello.nl', r'test42'),
        ('tmp', 'hippostech@gmail.com', r'test42'),
    )


def gather(list_of_name_tuples, upper_dir):
    for simple_name in os.listdir(upper_dir):
        longer_name = upper_dir + os.sep + simple_name
        if os.path.isdir(longer_name):
            gather(list_of_name_tuples, longer_name)
        else:
            list_of_name_tuples.append((simple_name, longer_name))


def main(Subscribers_class):
    subscribers = Subscribers_class()
    script_filename = sys.argv.pop(0)
    script_shortname = os.path.split(script_filename)[1]
    ok_commands = ('show', 'take', 'check', 'send', 'quit')
    command = (sys.argv and sys.argv.pop(0))
    if sys.stdout.isatty():
        if not command:
            command = 'check'
    else:
        print ("Content-type: text/html;charset=UTF-8\n\n") # the blank line really matters!
        command = 'show'
    if command not in ok_commands:
        putmsg("error: %s is not one of %s." %(command, ok_commands))
        sys.exit(999)
    cwd = os.getcwd()
    path_elements = cwd.split(os.sep)
    mailing_id = path_elements.pop()
    if path_elements.pop() != MagicMailTreeName:
        putmsg("warning: %s is not within a '%s' directory." %(mailing_id, MagicMailTreeName))
        # sys.exit(997)

    if command not in ('take',):
        dir_to_take_from = None
    else:
        if not sys.argv:
            putmsg("error: take requires directory argument.")
            sys.exit(998)
        dir_to_take_from = sys.argv.pop()
        files_to_take = []
        gather(files_to_take, dir_to_take_from)
        putmsg('\n'.join([str(t) for t in files_to_take]))

    # identify all possible attachments once only, before checking per-user.
    #
    # now look at each potential recipient in turn:
    #
    for name, email_addr, instrument_re in subscribers.what_goes_to_whom:
        try:
            files_to_attach = os.listdir(name)
        except FileNotFoundError:
            putmsg ("warning: no subdirectory for instrument group '%s' " % name)
            files_to_attach = None

        if dir_to_take_from:
# command 'take'
            if files_to_attach is None:
                putmsg("creating subdirectory for instrument group '%s' " % name)
                os.mkdir(name)
            if files_to_attach:
                putmsg("%u files/links are already present for instrument group '%s': %s"
                       % ( len(files_to_attach), name, files_to_attach))
            instrument_cre = re.compile(instrument_re)
            for simple_name, longer_name in files_to_take:
                if not instrument_cre.search(simple_name.lower()):
                    continue
                putmsg("putting symbolic link  to '%s' in subdirectory '%s'"
                          % (simple_name, name))
                try:
                    os.symlink(longer_name,
                           name + os.sep + simple_name)
                except FileExistsError:
                    putmsg ("warning: '%s' already exists in '%s' and will NOT be overwritten!"
                           %(simple_name, name))
            continue # that's all for take command!
# command 'check' or 'send'
        if not files_to_attach:
            # message below can get in the way, so maybe suppress it?:
            putmsg("I found nothing to attach so will not send mail at all to '%s'" % name)
            continue
        if not email_addr:
            putmsg ("We have no email address for %s."  % name)
            putmsg ("perhaps you need to putmsg the above would-be attachments?")
            continue
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        subject = subscribers.title.format(**locals())
        files_to_attach.sort()
        file_list = ",\n".join(['      %s' %filename for filename in files_to_attach])
        try:
            sender = subscribers.sender
        except AttributeError:
            sender = "Gill and Larry Myerscough"
        putmsg('preparing mail for intrument (group) "%s"' % name)
        putmsg('    mail subject will be "%s"' % subject)
        putmsg('    mail will appear to come from "%s"' % sender)
        putmsg('    mail recipient(s) will be "%s"' % email_addr)
        putmsg('    mail attachment(s) will be ...\n%s' % file_list)
        message_id_string = None
        msg['From'] = email.utils.formataddr((str(Header(sender, 'utf-8')), 'hippos@chello.nl'))
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
        if command in ("show",):
            src = "file://%s" % subscribers.sign_off_icon
        else:
            src = "cid:%s" % icon_content_id[1:-1]
        html_layout = str(
            h.html | ("\n",
                h.head | (
                ),
                h.body | (
                    h.p | subscribers.salutation,
                    h.p | subscribers.pre_text,
                    h.p | ([(name, h.br) for name in files_to_attach]),
                    h.p | (h.img(src=src), subscribers.sign_off),
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
        putmsg ("length of message is %u bytes" % len(bytes(msg)))
        if command in ('show',):
            print(str(html_layout))
        elif command in ('q', 'quit'):
            sys.exit(0)
        elif command in ('s', 'send',): # 'send' in sys.argv:
            with smtplib.SMTP('smtp.upcmail.nl') as s:
                s.send_message(msg)
                putmsg ("mail has been sent to '%s'." % email_addr)

if __name__ == '__main__':
    main(_Mailshot)
