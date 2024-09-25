import os
import configparser


class piPodConfiguration():
#    HomeDirectory = os.path.expanduser("~") + '/'
#    ConfigurationFile = 'piPod.conf'
#    ConfigurationFileLocation = HomeDirectory +  '.piPod/'
    
    def __init__(self):
        self.HomeDirectory  = os.path.expanduser("~") + '/'
        self.ConfigurationFile = 'piPod.conf'
        self.ConfigurationFileLocation = self.HomeDirectory +  '.piPod/'
#        self.ConfigurationFile = self.HomeDirectory +  '.piPod/piPod.conf'
        self.configuration = configparser.ConfigParser()
        self.configuration.sections()
        self.configuration.read(self.ConfigurationFileLocation + self.ConfigurationFile)
        
        # General Attributes
        self.WorkDirectory = os.path.join(self.HomeDirectory,  self.configuration['General']['WorkDirectory'])
        self.RelativeWorkDirectory = self.configuration['General']['WorkDirectory']
        self.ImageDirectory = os.path.join(self.HomeDirectory,  self.configuration['General']['ImageDirectory'])
        self.NoAlbumArt = self.configuration['General']['NoAlbumArt']
        self.InitWorkDirectory()
        
        #UI Attributes
        self.ThemeDirectory = os.path.join(self.HomeDirectory,  self.configuration['UI']['ThemeDirectory'])
        self.ThemeFile = self.configuration['UI']['ThemeFile']
        
        #Music Attributes
        self.MusicRootDirectory = os.path.join(self.HomeDirectory,  self.configuration['Music']['MusicRootDirectory'])
        self.PlaylistRootDirectory = self.HomeDirectory + self.configuration['Music']['PlaylistRootDirectory']
        self.PlaylistExtension = self.configuration['Music']['PlaylistExtension']
        
        #YouTubeMusic API (ytmusicapi) Attributes
        
        self.YouTubeDownloadOauthLocation = self.configuration['YouTubeMusic']['YouTubeOauthLocation']
        self.YouTubeDownloadOauthFile = self.configuration['YouTubeMusic']['YouTubeOauthFile']
        self.YouTubeDownloadOauthFileLocation = os.path.join(self.HomeDirectory,  self.YouTubeDownloadOauthLocation,  self.YouTubeDownloadOauthFile)
        
        #YouTubeDownLoader (yt-dlp) Attributes
        self.YouTubeDownloadCodec = self.configuration['YoutTubeDownloader']['DownloadCodec']
        self.PreferredDownloadQuality = self.configuration['YoutTubeDownloader']['PreferredDownloadQuality']
        self.YouTubeURL = self.configuration['YoutTubeDownloader']['YouTubeURL']
        self.CookieLocation =self.configuration['YoutTubeDownloader']['CookieLocation']
        self.CookieFile = self.configuration['YoutTubeDownloader']['CookieFile']
        self.CookieFileLocation = os.path.join(self.HomeDirectory, self.CookieLocation , self.CookieFile)
        self.YouTubeDownloadSource = self.configuration['YoutTubeDownloader']['Source']
        
        #MusicDB (TinyDB) Attributes
        self.MusicDBLocation = self.configuration['MusicDB']['MusicDBLocation']
        self.MusicDBFile = self.configuration['MusicDB']['MusicDBFile']
        self.MusicDBFileLocation = os.path.join(self.HomeDirectory, self.MusicDBLocation, self.MusicDBFile)
        
    def InitWorkDirectory(self):   
        if os.path.isdir(self.WorkDirectory) == False:
            mode = 0o666
            os.mkdir(self.WorkDirectory,  mode)



