#!/usr/bin/env python
"""  Widget derived from the Fraction Slider example of the pyqt tutorial book.
    Destined for use in my MusicRaft package
"""
import platform

from PyQt4 import (QtCore, QtGui)

X11 = hasattr(QtGui, 'qt_x11_wait_for_window_manager')

class Mark(QtGui.QWidget):

    WIDTH = 12.0
    HEIGHT = 10.0

    def __init__(self, parent=None, ix=0, tag='?', x=0, y=0):
        QtGui.QWidget.__init__(self, parent=parent)
        self.ix = ix
        self.tag = tag
        self.setGeometry(x, y, self.WIDTH, self.HEIGHT)
        self.show()

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        self.putShape(painter)
        self.putTag(painter)


    def putShape(self, painter):
        triangle = [QtCore.QPointF(0, 0),
                    QtCore.QPointF(self.WIDTH, 0.),
                    QtCore.QPointF(self.WIDTH/2, self.HEIGHT)]
        painter.setPen(QtCore.Qt.blue)
        painter.setBrush(QtCore.Qt.blue)
        painter.drawPolygon(QtGui.QPolygonF(triangle))


    def putTag(self, painter):
        pass  # for now!


    def mousePressEvent(self, event):
        #print('mousePressEvent', self.__class__.__name__, event.x(), self.x())
        self.parent().mousePressEvent(event, child=self)


    def mouseMoveEvent(self, event):
        #print('mouseMoveEvent', self.__class__.__name__, event.x(), self.x())
        self.parent().mouseMoveEvent(event, child=self)

class Bookmark(Mark):
    pass

class TimeMark(Mark):

    WIDTH = 12.0
    HEIGHT = 10.0

    def putShape(self, painter):
        painter.setPen(QtCore.Qt.red)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(0., 0., self.WIDTH, self.HEIGHT)


    def putTag(self, painter):
        pass  # for now!

class MarkedSlider(QtGui.QWidget):

    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"

    valueChanged = QtCore.pyqtSignal(int, int)

    def __init__(self, lowest=0, highest=100, value=0, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.__lowest = lowest
        self.__highest = highest
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                       QtGui.QSizePolicy.Fixed))
        self.marks = []
        self.setMarkList([dict(value=0, tag='T', Class=TimeMark)])

    def setMarkList(self, markList):
        self.markList = markList
        while self.marks:
            child = self.marks.pop()
            child.hide()
            child.deleteLater()

        for ix, dickie in enumerate(markList):
            Class = dickie.pop('Class', (ix and Bookmark or TimeMark))
            value = dickie.pop('value', 0)
            self.marks.append(Class(parent=self, ix=ix, x= self.xFromValue(value), **dickie))

    def span(self):
        return self.width() - (self.XMARGIN * 2)

    def range(self):
        return (self.__highest - self.__lowest)

    def xFromValue(self, value):
        return self.XMARGIN + (value*self.span()/self.range())

    def valueFromX(self, x):
        return (x-self.XMARGIN)*self.range()/self.span()

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        font = QtGui.QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QtGui.QFontMetricsF(font)
        return QtCore.QSize(# fm.width(BookmarkedSlider.WSTRING) *
                     # (self.__highest - self.__lowest),
                     480,
                     (fm.height() * 2) + self.YMARGIN)

    def setValue(self, value):
        if self.__lowest <= value <= self.__highest:
            self.__value = value
        else:
            raise ValueError("slider value out of range")
        self.update()
        self.updateGeometry()

    def mousePressEvent(self, event, child=None):
        # print ('mousePressEvent', self.__class__.__name__, event.x())
        if event.button() == QtCore.Qt.LeftButton:
            self.mouseMoveEvent(event, child=child)
            event.accept()
        else:
            QtGui.QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event, child=None):
        x = event.x()
        if child is None:
            child = self.marks[0]
        else:
            x += child.x()
        value = self.valueFromX(x)
        # print ('mouseMoveEvent', self.__class__.__name__, x, value)
        child.move(x, child.y())
        self.markList[child.ix]['value'] = value
        self.valueChanged.emit(child.ix, value)
        self.update()


    def keyPressEvent(self, event):
        change = 0
        if event.key() == QtCore.Qt.Key_Home:
            change = self.__lowest - self.__value
        elif event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Right):
            change = 1
        elif event.key() == QtCore.Qt.Key_PageUp:
            change = 10
        elif event.key() in (QtCore.Qt.Key_Down, QtCore.Qt.Key_Left):
            change = -1
        elif event.key() == QtCore.Qt.Key_PageDown:
            change = -10
        elif event.key() == QtCore.Qt.Key_End:
            change = self.__highest - self.__value
        if change:
            value = self.__value
            value += change
            if value != self.__value:
                self.__value = value
                self.valueChanged.emit(self.__value)
                self.update()
            event.accept()
        else:
            QtGui.QWidget.keyPressEvent(self, event)


    def paintEvent(self, event=None):
        font = QtGui.QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QtGui.QFontMetricsF(font)
        fracWidth = fm.width(self.WSTRING)
        indent = fm.boundingRect("9").width() / 2.0
        if not X11:
            fracWidth *= 1.5
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QtGui.QPalette.Mid))
        painter.setBrush(self.palette().brush(
                QtGui.QPalette.AlternateBase))
        painter.drawRect(self.rect())
        segColor = QtGui.QColor(QtCore.Qt.green).dark(120)
        segLineColor = segColor.dark()
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(self.XMARGIN,
                         self.YMARGIN, self.span(), fm.height())
        textColor = self.palette().color(QtGui.QPalette.Text)
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(self.WSTRING)
        yOffset = 0 #  segHeight #  + fm.height()
        painter.setPen(QtCore.Qt.yellow)
        painter.setBrush(QtCore.Qt.yellow)
        #value = self.markList[0]['value']
        #x = self.xFromValue(value)
        x = self.marks[0].x()
        painter.drawRect(self.XMARGIN, yOffset, x, fm.height())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    form = QtGui.QDialog()
    # form.setMaximumWidth(80)
    sliderLabel = QtGui.QLabel("Time")
    slider = MarkedSlider()
    slider2Label = QtGui.QLabel("Speed")
    slider2 = MarkedSlider()
    sliderLabel.setBuddy(slider)
    slider2Label.setBuddy(slider2)
    layout = QtGui.QGridLayout()
    layout.addWidget(sliderLabel, 0, 0)
    layout.addWidget(slider, 0, 1, 1, 3)
    layout.addWidget(slider2Label, 1, 0)
    layout.addWidget(slider2, 1, 1, 1, 3)
    form.setLayout(layout)

    def myValueChanged(ix, value):
        print ("value of mark", ix, "changed to", value)

    slider.valueChanged.connect(myValueChanged)

    myMarkList = [dict(Class=TimeMark, tag='t',  value=12),
                  dict(Class=Bookmark, tag='P',  value=52),
                  dict(Class=Bookmark, tag='Q',  value=54)]
    slider.setMarkList(myMarkList)
    form.setWindowTitle("Bookmarked Slider")
    form.show()
    app.exec_()

