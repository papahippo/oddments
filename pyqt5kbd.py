import sys
from PySide2.QtWidgets import (QApplication, QWidget)
from PySide2.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Space:
            print('Space key pressed')
        elif event.key() == Qt.Key_Left:
            print('Left Arrow key pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = MainWindow()
    demo.show()

    sys.exit(app.exec_())