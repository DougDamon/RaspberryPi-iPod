# File: main.py
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget 
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QPalette, QColor 
from events import Events
from pynput import keyboard

# def loadUiWidget(uifilename, parent=None):
    # print('QUiLoader')
    # loader = QUiLoader()
    # print(loader)
    # uifile = QFile(uifilename)
    # print(uifile)
    # uifile.open(QFile.ReadOnly)
    # print('open')
    # ui = loader.load(uifile, parent)
    # print('load')
    # uifile.close()
    # return ui
    
class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.ui_file_name = r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/piPodMainScreen.ui'
    
    # loader = QUiLoader(ui_file)
    # app = QApplication()
    # app = setButtonStyleSheet(app)
    def getUIFile(self):
        print(type(self))
        ui_file_location = r"C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/"
        ui_file_name = r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/piPodMainScreen.ui'
        ui_file = QFile(ui_file_name)
        print('Qfile')
        ui_file.open(QIODevice.ReadOnly)
        self.uiFile = ui_file
        # if not ui_file.open(QIODevice.ReadOnly):
            # print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            # sys.exit(-1)
        print('start load')
        # loader = QUiLoader()
        print(ui_file)
    def getWidget(self):
        w = QUiLoader().load(self.uiFile)
        print(w)
        ui_file.close()
        self.window = w
    
if __name__ == "__main__":
    # def loadUiWidget(uifilename, parent=None):
        # print('QUiLoader')
        # loader = QUiLoader()
        # print(loader)
        # uifile = QFile(uifilename)
        # print(uifile)
        # uifile.open(QFile.ReadOnly)
        # print('open')
        # ui = loader.load(uifile, parent)
        # print('load')
        # uifile.close()
        # return ui
        
    
    # print('app')
    mainScreen = MainScreen() 
    print('mainscreen')
    app = QApplication()
    mainScreen.getUIFile(r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/piPodMainScreen.ui')
    # app = QApplication()
    mainScreen.getWidget()
    print('loadui')
    mainScreen.show()
    mainScreen.pbNowPlaying.setFocus()
    mainScreen.pbNowPlaying.setAutoFillBackground(True)
    widget = mainScreen.focusWidget()
    print(widget)
    
    

    app.exec()