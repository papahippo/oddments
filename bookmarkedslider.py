#!/usr/bin/env python
# widget derived from the BookmarkedSlider example of the pyqt tutorial book.

import platform

from PyQt4.QtCore import (QPointF, QRectF, QSize, Qt, pyqtSignal)
from PyQt4.QtGui import (QApplication, QColor, QDialog, QFont,
        QFontMetricsF, QGridLayout, QLCDNumber, QLabel, QPainter,
        QPalette, QPolygonF, QSizePolicy, QSpinBox, QWidget)
X11 = True
try:
    from PyQt4.QtGui import qt_x11_wait_for_window_manager
except ImportError:
    X11 = False


class Mark(QWidget):

    WIDTH = 12.0
    HEIGHT = 10.0

    def __init__(self, parent=None, ix=0, tag='?', x=0, y=0):
        QWidget.__init__(self, parent=parent)
        self.ix = ix
        self.tag = tag
        self.setGeometry(x, y, self.WIDTH, self.HEIGHT)
        self.show()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        self.putShape(painter)
        self.putTag(painter)


    def putShape(self, painter):
        triangle = [QPointF(0, 0),
                    QPointF(self.WIDTH, 0.),
                    QPointF(self.WIDTH/2, self.HEIGHT)]
        painter.setPen(Qt.blue)
        painter.setBrush(Qt.blue)
        painter.drawPolygon(QPolygonF(triangle))


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
        painter.setPen(Qt.red)
        painter.setBrush(Qt.red)
        painter.drawRect(0., 0., self.WIDTH, self.HEIGHT)


    def putTag(self, painter):
        pass  # for now!

class MarkedSlider(QWidget):

    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"

    valueChanged = pyqtSignal(int, int)

    def __init__(self, lowest=0, highest=100, value=0, parent=None):
        QWidget.__init__(self, parent=parent)
        self.__lowest = lowest
        self.__highest = highest
        self.setFocusPolicy(Qt.WheelFocus)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.Fixed))

        self.setMarkList([dict(value=0, tag='T', Class=TimeMark)])

    def setMarkList(self, markList):
        self.markList = markList
        self.marks = []
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
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        return QSize(# fm.width(BookmarkedSlider.WSTRING) *
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
        if event.button() == Qt.LeftButton:
            self.mouseMoveEvent(event, child=child)
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event, child=None):
        x = event.x()
        if child is None:
            child = self.marks[0]
        else:
            x += child.x()
        value = self.valueFromX(x)
        print ('mouseMoveEvent', self.__class__.__name__, x, value)
        child.move(x, child.y())
        self.markList[child.ix]['value'] = value
        self.valueChanged.emit(child.ix, value)
        self.update()


    def keyPressEvent(self, event):
        change = 0
        if event.key() == Qt.Key_Home:
            change = self.__lowest - self.__value
        elif event.key() in (Qt.Key_Up, Qt.Key_Right):
            change = 1
        elif event.key() == Qt.Key_PageUp:
            change = 10
        elif event.key() in (Qt.Key_Down, Qt.Key_Left):
            change = -1
        elif event.key() == Qt.Key_PageDown:
            change = -10
        elif event.key() == Qt.Key_End:
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
            QWidget.keyPressEvent(self, event)


    def paintEvent(self, event=None):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        fracWidth = fm.width(self.WSTRING)
        indent = fm.boundingRect("9").width() / 2.0
        if not X11:
            fracWidth *= 1.5
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QPalette.Mid))
        painter.setBrush(self.palette().brush(
                QPalette.AlternateBase))
        painter.drawRect(self.rect())
        segColor = QColor(Qt.green).dark(120)
        segLineColor = segColor.dark()
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(self.XMARGIN,
                         self.YMARGIN, self.span(), fm.height())
        textColor = self.palette().color(QPalette.Text)
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(self.WSTRING)
        yOffset = 0 #  segHeight #  + fm.height()
        painter.setPen(Qt.yellow)
        painter.setBrush(Qt.yellow)
        #value = self.markList[0]['value']
        #x = self.xFromValue(value)
        x = self.marks[0].x()
        painter.drawRect(self.XMARGIN, yOffset, x, fm.height())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = QDialog()
    # form.setMaximumWidth(80)
    sliderLabel = QLabel("&Fraction?")
    slider = MarkedSlider(value=42)
    sliderLabel.setBuddy(slider)
    layout = QGridLayout()
    layout.addWidget(sliderLabel, 0, 0)
    layout.addWidget(slider, 0, 1, 1, 3)
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

