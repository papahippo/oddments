#!/usr/bin/env python3
from PyQt4 import QtCore, QtGui
import socket

acpi_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
acpi_sock.connect('/var/run/acpid.socket')

def got_acpi_notification():
    # print ("got_acpi_notification")
    new_stuff = acpi_sock.recv(4096)
    # print(new_stuff)
    for event in new_stuff.decode().split('\n'):
        terms = event.split(' ')
        if not terms[0].startswith('jack'):
            continue
        print(terms)

app = QtGui.QApplication([])

notifier = QtCore.QSocketNotifier(acpi_sock.fileno(), QtCore.QSocketNotifier.Read)
notifier.activated.connect(got_acpi_notification)

w = QtGui.QMainWindow()
w.show()
app.exec_()
acpi_sock.close()

