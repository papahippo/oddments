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


class Bookmark(QWidget):

    WIDTH = 12.0
    HEIGHT = 10.0

    def __init__(self, parent=None, x=0, y=0):
        QWidget.__init__(self, parent=parent)
        self.move(x, y)
        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)
        self.show()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        self.putShape(painter)
        self.putTag(painter)


    def putShape(self, painter):
        triangle = [QPointF(0, 0),
                    QPointF(self.WIDTH, 0.),
                    QPointF(self.WIDTH/2, self.HEIGHT)]
        painter.setPen(Qt.yellow)
        painter.setBrush(Qt.darkYellow)
        painter.drawPolygon(QPolygonF(triangle))


    def putTag(self, painter):
        pass  # for now!

class BookmarkedSlider(QWidget):

    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"

    valueChanged = pyqtSignal(int)

    def __init__(self, lowest=0, highest=100, value=0, parent=None):
        super(BookmarkedSlider, self).__init__(parent)
        self.__lowest = lowest
        self.__highest = highest
        self.__value = value
        self.setFocusPolicy(Qt.WheelFocus)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.Fixed))
        self.bookmarks = [Bookmark(self, 52), Bookmark(self, 252)]

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
                     (fm.height() * 2) + BookmarkedSlider.YMARGIN)

    def setValue(self, value):
        if self.__lowest <= value <= self.__highest:
            self.__value = value
        else:
            raise ValueError("slider value out of range")
        self.update()
        self.updateGeometry()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.moveSlider(event.x())


    def moveSlider(self, x):
        value = self.valueFromX(x)
        print(x, value)
        if value != self.__value:
            self.__value = value
            self.valueChanged.emit(self.__value)
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
        fracWidth = fm.width(BookmarkedSlider.WSTRING)
        indent = fm.boundingRect("9").width() / 2.0
        if not X11:
            fracWidth *= 1.5
        value = self.__value
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
        painter.drawRect(BookmarkedSlider.XMARGIN,
                         BookmarkedSlider.YMARGIN, self.span(), fm.height())
        textColor = self.palette().color(QPalette.Text)
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(BookmarkedSlider.WSTRING)
        x = BookmarkedSlider.XMARGIN
        yOffset = 0 #  segHeight #  + fm.height()
        painter.setPen(Qt.yellow)
        painter.setBrush(Qt.darkYellow)
        painter.drawRect(x, yOffset, self.xFromValue(value), fm.height())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = QDialog()
    # form.setMaximumWidth(80)
    sliderLabel = QLabel("&Fraction?")
    slider = BookmarkedSlider(value=42)
    sliderLabel.setBuddy(slider)
    layout = QGridLayout()
    layout.addWidget(sliderLabel, 0, 0)
    layout.addWidget(slider, 0, 1, 1, 3)
    form.setLayout(layout)

    def valueChanged(value):
        slider.setValue(value)

    form.setWindowTitle("Bookmarked Slider")
    form.show()
    app.exec_()

