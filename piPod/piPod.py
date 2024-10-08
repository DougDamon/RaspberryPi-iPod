import sys
#from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow #, QWidget 
# from PySide2.QtCore import QFile, QIODevice
# from PySide2.QtGui import QPalette, QColor 
# from PySide6.uic import loadUi 
#from events import Events
#from pynput import keyboard

from gui.ui_piPodMainScreen import Ui_wMainScreen
from gui.ui_piPodNowPlayingScreen import Ui_wNowPlaying

class NowPlayingWindow(QMainWindow, Ui_wNowPlaying):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.connectSignalsSlots()
        
class MainScreen(QMainWindow, Ui_wMainScreen):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.connectSignalsSlots()
        #self.centralwidget.pbNowPlaying.click.connect(self.now_playing_clicked)
        self.now_playing = NowPlayingWindow(self)
        
#   def connectSignalsSlots(self):
#        self.action_Exit.triggered.connect(self.close)
#        self.action_Find_Replace.triggered.connect(self.findAndReplace)
#        self.action_About.triggered.connect(self.about)

    def now_playing_clicked(self):
        self.now_playing.show()
        self.hide()
        
        

def main():        
    app = QApplication(sys.argv)
    win = MainScreen()
    win.show()
    sys.exit(app.exec_())
            
    
if __name__ == "__main__":
    main()
