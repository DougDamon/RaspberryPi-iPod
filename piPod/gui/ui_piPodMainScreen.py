# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'piPodMainScreenkWgByz.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_wMainScreen(object):
    def setupUi(self, wMainScreen):
        if not wMainScreen.objectName():
            wMainScreen.setObjectName(u"wMainScreen")
        wMainScreen.setWindowModality(Qt.ApplicationModal)
        wMainScreen.resize(320, 240)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wMainScreen.sizePolicy().hasHeightForWidth())
        wMainScreen.setSizePolicy(sizePolicy)
        wMainScreen.setMinimumSize(QSize(320, 240))
        wMainScreen.setMaximumSize(QSize(320, 240))
        wMainScreen.setSizeIncrement(QSize(320, 240))
        wMainScreen.setBaseSize(QSize(320, 240))
        icon = QIcon()
        iconThemeName = u"accessories-calculator"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        wMainScreen.setWindowIcon(icon)
        wMainScreen.setStyleSheet(u"QPushButton {background-color:white;\n"
"        border-color: blue;\n"
"        border: 0px;}\n"
"QPushButton:focus {background-color: rgb(85, 170, 255);\n"
"        border-color: black;}")
        self.centralwidget = QWidget(wMainScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.pbNowPlaying = QPushButton(self.centralwidget)
        self.pbNowPlaying.setObjectName(u"pbNowPlaying")
        self.pbNowPlaying.setGeometry(QRect(12, 0, 300, 24))
        sizePolicy.setHeightForWidth(self.pbNowPlaying.sizePolicy().hasHeightForWidth())
        self.pbNowPlaying.setSizePolicy(sizePolicy)
        self.pbNowPlaying.setAutoFillBackground(False)
        self.pbNowPlaying.setStyleSheet(u"")
        self.pbNowPlaying.setFlat(False)
        self.pbMusic = QPushButton(self.centralwidget)
        self.pbMusic.setObjectName(u"pbMusic")
        self.pbMusic.setGeometry(QRect(12, 30, 300, 24))
        sizePolicy.setHeightForWidth(self.pbMusic.sizePolicy().hasHeightForWidth())
        self.pbMusic.setSizePolicy(sizePolicy)
        self.pbMusic.setFlat(False)
        self.pbOTR = QPushButton(self.centralwidget)
        self.pbOTR.setObjectName(u"pbOTR")
        self.pbOTR.setGeometry(QRect(12, 60, 300, 24))
        sizePolicy.setHeightForWidth(self.pbOTR.sizePolicy().hasHeightForWidth())
        self.pbOTR.setSizePolicy(sizePolicy)
        self.pbOTR.setFlat(False)
        self.pbAudiobooks = QPushButton(self.centralwidget)
        self.pbAudiobooks.setObjectName(u"pbAudiobooks")
        self.pbAudiobooks.setGeometry(QRect(12, 90, 300, 24))
        sizePolicy.setHeightForWidth(self.pbAudiobooks.sizePolicy().hasHeightForWidth())
        self.pbAudiobooks.setSizePolicy(sizePolicy)
        self.pbAudiobooks.setAutoDefault(False)
        self.pbAudiobooks.setFlat(False)
        self.pbGames = QPushButton(self.centralwidget)
        self.pbGames.setObjectName(u"pbGames")
        self.pbGames.setGeometry(QRect(12, 120, 300, 24))
        sizePolicy.setHeightForWidth(self.pbGames.sizePolicy().hasHeightForWidth())
        self.pbGames.setSizePolicy(sizePolicy)
        self.pbGames.setFlat(False)
        self.pbSettings = QPushButton(self.centralwidget)
        self.pbSettings.setObjectName(u"pbSettings")
        self.pbSettings.setGeometry(QRect(12, 150, 300, 24))
        sizePolicy.setHeightForWidth(self.pbSettings.sizePolicy().hasHeightForWidth())
        self.pbSettings.setSizePolicy(sizePolicy)
        self.pbSettings.setFocusPolicy(Qt.StrongFocus)
        self.pbSettings.setContextMenuPolicy(Qt.NoContextMenu)
        self.pbSettings.setFlat(False)
        wMainScreen.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(wMainScreen)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 320, 28))
        wMainScreen.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(wMainScreen)
        self.statusbar.setObjectName(u"statusbar")
        wMainScreen.setStatusBar(self.statusbar)

        self.retranslateUi(wMainScreen)
        self.pbNowPlaying.clicked.connect(wMainScreen.now_playing_clicked)

        self.pbNowPlaying.setDefault(False)
        self.pbAudiobooks.setDefault(False)


        QMetaObject.connectSlotsByName(wMainScreen)
    # setupUi

    def retranslateUi(self, wMainScreen):
        wMainScreen.setWindowTitle("")
        self.pbNowPlaying.setText(QCoreApplication.translate("wMainScreen", u"Now Playing", None))
        self.pbMusic.setText(QCoreApplication.translate("wMainScreen", u"Music", None))
        self.pbOTR.setText(QCoreApplication.translate("wMainScreen", u"OTR", None))
        self.pbAudiobooks.setText(QCoreApplication.translate("wMainScreen", u"Audiobooks", None))
        self.pbGames.setText(QCoreApplication.translate("wMainScreen", u"Gamess", None))
        self.pbSettings.setText(QCoreApplication.translate("wMainScreen", u"Settings", None))
    # retranslateUi

