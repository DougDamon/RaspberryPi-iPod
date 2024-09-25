from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Signal, Slot
from PySide6.QtWidgets import QApplication
import sys
ui_loc = r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/'
main_screen_loc = ui_loc + r'piPodMainScreen.ui'
now_playing_loc = ui_loc + r'piPodNowPlayingScreen.ui'

def now_playing_ispressed():
    main_screen_ui.hide()
    now_playing_ui.show()
    
if __name__ == "__main__":
    loader = QUiLoader()
    app = QApplication(sys.argv)
    # file = QFile(r'C:/Users/ddamon/OneDrive - Callon Petroleum Company/Documents/Personal/piPod/piPodMainScreen.ui')
    ###### load screens #####
    # main screens
    main_screen_file = QFile(main_screen_loc) 
    main_screen_file.open(QFile.ReadOnly)
    main_screen_ui = loader.load(main_screen_file)
    main_screen_file.close()
    # now playing screens
    now_playing_file = QFile(now_playing_loc) 
    now_playing_file.open(QFile.ReadOnly)
    now_playing_ui = loader.load(main_screen_file)
    now_playing_file.close()
    main_screen_ui.show()
    sys.exit(app.exec())