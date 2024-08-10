# File: main.py
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtGui import QPalette, QColor 
from events import Events
from pynput import keyboard
   
# class MainScreen(QApplication):
    
if __name__ == "__main__":
    
    
    # ui_file_location = r"C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/"
    ui_file_name = r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/piPodMainScreen.ui'
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    app = QApplication(sys.argv)
    # loader = QUiLoader()
    # app = setButtonStyleSheet(app)
    # window = loader.load(ui_file_name)
    window = QUiLoader().load(ui_file_name)
    
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    
    
    
    window.show()
    window.pbNowPlaying.setFocus()
    window.pbNowPlaying.setAutoFillBackground(True)
    widget = QApplication.focusWidget()
    print(widget)
    
    

    sys.exit(app.exec())
