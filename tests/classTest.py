# File: main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget 
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QMetaObject
from PySide6.QtGui import QPalette, QColor 
from events import Events
from pynput import keyboard

class UiLoader(QUiLoader):
    _baseinstance = None
    print('a')

    def createWidget(self, classname, parent=None, name=''):
        if parent is None and self._baseinstance is not None:
            widget = self._baseinstance
        else:
            widget = super().createWidget(classname, parent, name)
            if self._baseinstance is not None:
                setattr(self._baseinstance, name, widget)
        return widget

    def loadUi(self, uifile, baseinstance=None):
        print('b')
        self._baseinstance = baseinstance
        widget = self.load(uifile)
        QMetaObject.connectSlotsByName(baseinstance)
        return widget
        
class MainWindow(QMainWindow):
    ui_file_name = r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/piPodMainScreen.ui'
    def __init__(self):
        super().__init__()
        print('1')
        loader = UiLoader()
        app = QApplication(['piPod'])
        print('2')
        # loader.registerCustomWidget(MyLabel)
        loader.loadUi(ui_file_name, self)
        print('3')

    # @QtCore.Slot()
    # def on_testButton_clicked(self):
        # self.customLabel.setText(
            # '' if self.customLabel.text() else 'Hello World')

if __name__ == '__main__':
    print('a')
    window = MainWindow()
    print('b')
    window.show()
    try:
        app.exec()
    except AttributeError:
        app.exec_()