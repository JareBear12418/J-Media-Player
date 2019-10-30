#pip install playsound
from playsound import playsound
# pip install pyqt5
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui, sip
import sys
# playsound('Music Player/test_audio.mp3')
print('its working')
title = 'CNC Bit Config'
version = 'v0.01'
class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.title = title
        self.version = version
        self.width = canvas_width
        self.height = canvas_height
        self.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)
        self.initUI()
        
    def initUI(self):
        label = QtGui.QLabel('My Label')
        line_edit = QtGui.QLineEdit()

        form_layout = QtGui.QFormLayout()
        form_layout.addRow(label, line_edit)

        close_button = QtGui.QPushButton('Close')
        execute_button = QtGui.QPushButton('Execute')

        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(close_button)
        button_layout.addWidget(execute_button)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())
