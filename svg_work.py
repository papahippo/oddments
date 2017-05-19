#/usr/bin/python
# -*- coding: utf-8 -*-
"""
Goal is to process svg output relating to ABC music sources in a more robust way than currently
doone within 'Musicraft'. When a workable solution is found, it will be incorporated into
'Musicraft'.
'Borrowed'...
http://stackoverflow.com/questions/13125398/alternative-for-scripting-in-svg-for-using-in-python
.. as starting point; thanks!
"""
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtWebKit import QGraphicsWebView
class Scene(QtGui.QGraphicsScene):
    def __init__(self):
        super(QtGui.QGraphicsScene, self).__init__()
        self.view = QtGui.QGraphicsView(self)

        self.webview = QGraphicsWebView()
        self.webview.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
        self.webview.setCacheMode(QtGui.QGraphicsItem.NoCache)
        self.addItem(self.webview)

        self.webview.loadFinished.connect(self.svgLoaded)

    def svgLoaded(self):
        frame = self.webview.page().mainFrame()
        fsize = frame.contentsSize()
        self.webview.resize(QtCore.QSizeF(fsize))
        self.view.resize(fsize.width() + 10, fsize.height() + 10)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    v = Scene()
    svg = QtCore.QUrl("test.svg")
    v.webview.load(svg)
    v.view.show()
    sys.exit(app.exec_())
