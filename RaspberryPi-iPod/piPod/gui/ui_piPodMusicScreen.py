# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'piPodMusicScreenhFySun.ui'
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
        self.centralwidget = QWidget(wMainScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.pbNowPlaying = QPushButton(self.centralwidget)
        self.pbNowPlaying.setObjectName(u"pbNowPlaying")
        self.pbNowPlaying.setGeometry(QRect(12, 0, 300, 24))
        sizePolicy.setHeightForWidth(self.pbNowPlaying.sizePolicy().hasHeightForWidth())
        self.pbNowPlaying.setSizePolicy(sizePolicy)
        self.pbAlbums = QPushButton(self.centralwidget)
        self.pbAlbums.setObjectName(u"pbAlbums")
        self.pbAlbums.setGeometry(QRect(12, 30, 300, 24))
        sizePolicy.setHeightForWidth(self.pbAlbums.sizePolicy().hasHeightForWidth())
        self.pbAlbums.setSizePolicy(sizePolicy)
        self.pbArtists = QPushButton(self.centralwidget)
        self.pbArtists.setObjectName(u"pbArtists")
        self.pbArtists.setGeometry(QRect(12, 60, 300, 24))
        sizePolicy.setHeightForWidth(self.pbArtists.sizePolicy().hasHeightForWidth())
        self.pbArtists.setSizePolicy(sizePolicy)
        self.pbArtists.setFlat(False)
        self.pbGenre = QPushButton(self.centralwidget)
        self.pbGenre.setObjectName(u"pbGenre")
        self.pbGenre.setGeometry(QRect(12, 90, 300, 24))
        sizePolicy.setHeightForWidth(self.pbGenre.sizePolicy().hasHeightForWidth())
        self.pbGenre.setSizePolicy(sizePolicy)
        self.pbGenre.setAutoDefault(False)
        self.pbGenre.setFlat(False)
        self.pbPlaylists = QPushButton(self.centralwidget)
        self.pbPlaylists.setObjectName(u"pbPlaylists")
        self.pbPlaylists.setGeometry(QRect(12, 120, 300, 24))
        sizePolicy.setHeightForWidth(self.pbPlaylists.sizePolicy().hasHeightForWidth())
        self.pbPlaylists.setSizePolicy(sizePolicy)
        self.pbSongs = QPushButton(self.centralwidget)
        self.pbSongs.setObjectName(u"pbSongs")
        self.pbSongs.setGeometry(QRect(12, 150, 300, 24))
        sizePolicy.setHeightForWidth(self.pbSongs.sizePolicy().hasHeightForWidth())
        self.pbSongs.setSizePolicy(sizePolicy)
        self.pbSongs.setFocusPolicy(Qt.StrongFocus)
        self.pbSongs.setContextMenuPolicy(Qt.NoContextMenu)
        wMainScreen.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(wMainScreen)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 320, 28))
        wMainScreen.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(wMainScreen)
        self.statusbar.setObjectName(u"statusbar")
        wMainScreen.setStatusBar(self.statusbar)

        self.retranslateUi(wMainScreen)

        self.pbGenre.setDefault(False)


        QMetaObject.connectSlotsByName(wMainScreen)
    # setupUi

    def retranslateUi(self, wMainScreen):
        wMainScreen.setWindowTitle("")
        self.pbNowPlaying.setText(QCoreApplication.translate("wMainScreen", u"Now Playing", None))
        self.pbAlbums.setText(QCoreApplication.translate("wMainScreen", u"Albums", None))
        self.pbArtists.setText(QCoreApplication.translate("wMainScreen", u"Artists", None))
        self.pbGenre.setText(QCoreApplication.translate("wMainScreen", u"Genre", None))
        self.pbPlaylists.setText(QCoreApplication.translate("wMainScreen", u"Playlists", None))
        self.pbSongs.setText(QCoreApplication.translate("wMainScreen", u"Songs", None))
    # retranslateUi

