import sys
import os.path
from optparse import OptionParser
from PyKDE4.kdecore import *
from PyQt4 import Qt


def mime_type_hierarchy(mime_type):
    ret = []
    while mime_type != '':
        ret.append(str(mime_type))
        mime_type = KMimeType.mimeType(mime_type).parentMimeType()
    return ret


def main(options, expr):
    if options.mime:
        print(
        mime_type_hierarchy(expr))
        for app in KMimeTypeTrader.self().query(expr):
            print(
            app.desktopEntryPath())
    elif options.application:
        for x in KService.serviceByStorageId(expr).serviceTypes():
            print(x)
    elif options.file:
        mime, accuracy = KMimeType.findByPath(expr)
        print(
        "Mime-type: %s, Accuracy: %d" % (mime.name(), accuracy))


if __name__ == "__main__":
    usage = "Usage: %prog [options] EXPR"
    version = "%prog-0.1\n2010 \xc2\xa9 Guy Rutenberg "
    parser = OptionParser(usage, version=version)
    parser.add_option("-m", "--mime-type", dest="mime", default=False,
                      action="store_true",
                      help="Show the MIME type hierarchy and associated applications for a given MIME type")
    parser.add_option("-a", "--application", dest="application", default=False,
                      action="store_true",
                      help="Print associated MIME types for a given application")
    parser.add_option("-f", "--file", dest="file", default=False,
                      action="store_true",
                      help="See the MIME type associated with a given file")
    (options, args) = parser.parse_args(args=sys.argv)

    if len(args) < 2:
        sys.stderr.write(usage + "\n")
        sys.exit(1)
    # this is required to prevent a warning message when using KDE functions
    a = Qt.QApplication(sys.argv)
    main(options, *args[1:])