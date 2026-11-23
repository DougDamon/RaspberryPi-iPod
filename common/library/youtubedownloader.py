# on start delete all mp3 and image files
# * Get Artwork
# * Apply Artwork to tags
# Rename song file
# move song to Root/Artist/Album/Song
# create/update playlist
# check if song exists before download
# think about failures and reasonable error codes.
# get oauth - read to figure out how that works with google
# configuration downloadtmpdir, youtubeurl, musicRootDir, playlistRootDir

import os
from ytmusicapi import YTMusic
import yt_dlp
import music_tag
#import urllib.request
from urllib.request import urlopen
#from PIL import Image
import glob
import io
#from datetime import datetime
#from difflib import SequenceMatcher
from common.audio.mpd_player import MPDAudioPlayback
from common.config.settings import ConfigService
from common.library.music_database import MusicDB

class YouTubeDownloader():
    def __init__(self):
        self.musicDB = MusicDB()
        self.mpd = MPDAudioPlayback()
        self.config = ConfigService()
        self.YouTubeMusicSource = self.config.YouTubeDownloadSource
        self.WorkDirectory = self.config.WorkDirectory
        self.RelativeWorkDirectory = self.config.RelativeWorkDirectory

        self.MusicRootDirectory = self.config.MusicRootDirectory
        self.YouTubeDowloadCodec = self.config.YouTubeDownloadCodec
        self.PlaylistExtension = self.config.PlaylistExtension
        self.PlaylistRootDirectory = self.config.PlaylistRootDirectory
        self.YouTubeURL = self.config.YouTubeURL
        self.OauthFileLocation = self.config.YouTubeDownloadOauthFileLocation
        self.CookieFileLocation = self.config.CookieFileLocation
        self.PreferredQuality = self.config.PreferredDownloadQuality
#        sTinyDBFileLocation = config.MusicDBFileLocation
        self.Codec = self.config.YouTubeDownloadCodec
        self.sTrackNumber = ''
        self.YouTubeAuth = self.getYouTubeAutorization()
        
    def nvl(var, val):
        if var is None:
            return val
        else:
            return var
  
    def nvl2(var, isNotNone, isNone):
        if var is None:
            return isNone
        else:
            return isNotNone
                
    def getYouTubeAutorization(self):
        return YTMusic(
            self.config.YouTubeDownloadOauthFileLocation
        )
 
    def getLibraryPlaylistsFromYouTube(self):
        libraryPlaylists = self.YouTubeAuth.get_library_playlists(limit=None)
    
        playlists = []
    
        for playlist in libraryPlaylists:
            playlist_id = playlist['playlistId']
    
            if playlist_id == 'SS':
                continue
    
            playlists.append({
                'id': playlist_id,
                'title': playlist['title']
            })
    
        return playlists
 
    def downloadLibraryPlaylistsFromYouTube(self):
        libraryPlaylists = self.YouTubeAuth.get_library_playlists()
        for userPlaylist in libraryPlaylists:
            print(userPlaylist['title'])
            downloadPlaylistId = userPlaylist['playlistId']
            if  downloadPlaylistId == 'SS':
                continue
            downloadPlaylist = self.getPlaylistFromYouTube(downloadPlaylistId)
            self.musicDB.addPlaylistToDB(downloadPlaylist,  self.YouTubeMusicSource)
            

    def getPlaylistFromYouTube(self, downloadPlaylistId):
        userPlaylist = self.YouTubeAuth.get_playlist(downloadPlaylistId)
        return userPlaylist
    
    def searchSubstituteTrackInYouTubeMusic(self, Track):
        sTrackName = Track['title']
        sArtist = Track['artists'][0]['name']
    
        if sArtist is None:
            sArtist = "Unknown Artist"
    
        if Track['album'] is None:
            sSearchString = sTrackName + ' ' + sArtist
        else:
            sAlbum = Track['album']['name']
            sSearchString = (
                sTrackName
                + ' '
                + sArtist
                + ' '
                + sAlbum
            )
    
        sSearchFilter = 'songs'
    
        searchResults = self.YouTubeAuth.search(
            sSearchString,
            sSearchFilter
        )
    
        if len(searchResults) == 0:
            return {}
    
        return searchResults[0]
    
    def trackExists( self, fileSystemTrackDirectory, currentFileSystemTrackName):
        trackLocation = os.path.join(
            fileSystemTrackDirectory,
            currentFileSystemTrackName
        )
    
        return os.path.isfile(trackLocation)
    
    def downloadPlaylistTracksFromYouTube(self, downloadPlaylist):
        sPlaylistId = downloadPlaylist ['id']
        self.musicDB.removePlaylistTracksFromDB(sPlaylistId)
        iTrackPlaybackOrder = 0
        tracks= downloadPlaylist['tracks']
        for currentTrack in tracks:
            downloadTrack = currentTrack
            if downloadTrack['album'] is not None:
                if downloadTrack['album']['id'][0:5] != 'MPREb':
                    downloadTrack = self.searchSubstituteTrackInYouTubeMusic(currentTrack)
            if len(downloadTrack) > 0:
                currentAlbum = self.getTrackAlbum(downloadTrack)
                currentFileSystemTrackDirectory = self.getFileSystemDirectoryName(self.MusicRootDirectory,  downloadTrack)
                currentFileSystemTrackName = self.getFileSystemTrackName(currentAlbum, downloadTrack, self.Codec)
                if not self.trackExists(currentFileSystemTrackDirectory,  currentFileSystemTrackName):
                    self.downloadTrackFromYouTube(downloadPlaylist,  downloadTrack)
                iTrackPlaybackOrder += 1

                self.musicDB.addYouTubeTrackToDB(
                    downloadPlaylist,
                    currentAlbum,
                    downloadTrack,
                    iTrackPlaybackOrder,
                    currentFileSystemTrackDirectory,
                    currentFileSystemTrackName
                )

    def downloadPlaylistFromYouTube(self, downloadPlaylistId):
        youTubePlaylist = self.getPlaylistFromYouTube(
            downloadPlaylistId
        )
    
        self.downloadPlaylistTracksFromYouTube(
            youTubePlaylist
        )
    
        self.musicDB.setPlaylistDownloaded(
            downloadPlaylistId
        )
    
        print("Updating MPD library...")
        self.mpd.update_library()
        print("MPD library update started.")

#def getAlbumFromDB(albumId):
#    albumTable = getTable('Album')
#    albumQuery = Query()
#    album = albumTable.search(albumQuery.albumTable.AlbumId == albumId )
#    return album

    def getAlbumName(self,  track):
        if track['album'] is None:
            albumName = 'Unknown' # YouTubeSong['title']
        else:
            albumName = track['album']['name']
        return albumName
    
    def getAlbumTrackNumber(self,  album, track):
    # ytAlbum = YouTubeConnection.get_album(YouTubeSong['album']['id'])
    # print(YouTubeAlbum)
        if album is None:
            trackNumber = '00'
        else:
            i = 1
            for albumTrack in album['tracks']:
                if albumTrack['videoId'] == track['videoId']:
                    if len(str(i)) == 1:
                        trackNumber = '0' + str(i)
                    else:
                        trackNumber = str(i)
            i += 1
        return trackNumber

    def getFileSystemDirectoryName(
        self,
        rootMusicDirectory,
        track
    ):
        artist = track['artists'][0]['name']
    
        if artist is None:
            artist = 'Unknown Artist'
    
        if track['album'] is None:
            return os.path.join(
                rootMusicDirectory,
                'YouTube'
            )
    
        return os.path.join(
            rootMusicDirectory,
            artist,
            track['album']['name']
        )

    def getFileSystemTrackName(self,  album, track,  codec):
        # song file name format if metadata is available: Artist_Album_TrackNumber_SongName[.mp3] - file extension not included
        # song file name format if metadata is incomplete: Artist_YoutubeTitle_VidId.mp3
        isYouTubeVideo = False
        trackName = track['title']
        if track['artists'][0]['name'] is None:
            artist = 'Unknown'
        else:
            artist = track['artists'][0]['name']

        if track['album'] is None:
            # assume this is a user loaded video
            isYouTubeVideo = True
            sVidID = str(track['videoId'])
        else:
            albumName = track['album']['name']
            trackNumber = self.getAlbumTrackNumber(album, track)

        if isYouTubeVideo == False:
            fileSystemTrackName = artist + '_' + albumName + '_' + trackNumber + '_' + trackName
        else:
            fileSystemTrackName = artist + '_' + trackName + '_' + sVidID

        return fileSystemTrackName + '.' + codec

    def downloadAudioFromYouTube(self, yt_url):
        # yt_dl only seems to work with a relative changing manually to '~' from current directory
        # setting the work directory and then changing back to the 
    #    sCurrentDirectory = os.getcwd()
    #    print(sCurrentDirectory)
    #    print()
    #    print(sWorkDirectory)
    #    print()
    #    os.chdir(sWorkDirectory)
        ydl_opts = {
            # 'cookiesfrombrowser' : 'chrome',
            'cookiefile' : self.CookieFileLocation, 
            'format': 'bestaudio/best',
            'outtmpl': self.WorkDirectory + '%(title)s.%(ext)s',
#           'outtmpl':  'home/doug/.piPod/tmp/'+ '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.Codec,
                'preferredquality': self.PreferredQuality,
            }],
        }
        print(ydl_opts)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
#    os.chdir(sCurrentDirectory)

    def getNewestDownloadedFilename(self,  directory):
        pattern = os.path.join(
            directory,
            '*.' + self.Codec
        )
    
        downloaded_files = glob.glob(
            pattern
        )
    
        return max(
            downloaded_files,
            key=os.path.getctime
        )


    def setId3Tags(self, album, track, downloadFile):
        try:
            currentTrack = music_tag.load_file(downloadFile)
        except OSError as error :
            print(error)
            print('Error opening file: ' + downloadFile)
        currentTrack['title'] = track['title']
        currentTrack['artist'] = track['artists'][0]['name']
        if track['album'] is None:
            currentTrack['album'] = 'Unknown Album'
            currentTrack['comment'] = (
                'YouTube track with no album metadata'
            )
        
            thumbnails = track.get(
                'thumbnails',
                []
            )
        
            if len(thumbnails) > 0:
                imgLoc = thumbnails[-1]
        
                tmp = urlopen(
                    imgLoc['url']
                )
        
                data = bytearray(
                    tmp.read()
                )
        
                currentTrack['artwork'] = io.BytesIO(
                    data
                ).getvalue()
        else:
            currentTrack['album'] = track['album']['name']
#           yt = getYouTubeAutorization()
            album = self.YouTubeAuth.get_album(track['album']['id'])
            currentTrack['totaltracks'] = album['trackCount']
            currentTrack['year'] = album['year']
            try:
                currentTrack['comment'] = album['description']
            except KeyError:
                currentTrack['comment'] = 'Most likey user uploaded video.  No Song or Album information available'
            currentTrack['albumartist'] = album['artists'][0]['name']
            # print(album.keys())
            # i = 1
            # for track in album['tracks']:
            #     if track['videoId'] == song['videoId']:
            #         if len(str(i)) == 1:
            #             sTrackNumber = '0' + str(i)
            #         else:
            #             sTrackNumber = str(i)
            #             currentSongTags['tracknumber'] = sTrackNumber
            # i += 1
            currentTrack['tracknumber'] = self.getAlbumTrackNumber(album, track)
#           art = currentSongTags['artwork']
            # print(art)
            # print(YouTubeAlbum['thumbnails'][-1])
            imgLoc = album['thumbnails'][-1]
            tmp = urlopen(imgLoc['url'])
            data = bytearray(tmp.read())
            currentTrack['artwork'] = io.BytesIO(data).getvalue()
            # i = 0
            # for imgLoc in YouTubeAlbum['thumbnails']:
            #     tmp = urlopen(imgLoc['url'])
            #     data = bytearray(tmp.read())
            #     # print(imgLoc)
            #     # print(data)
            #     # Image.
            #     image = Image.open(io.BytesIO(data))
            #     # art.values(i).thumbnail([imageWidth, imageHeight]) == data
            #     if i == 0:
            #         # with open(image, 'rb') as img_in:
            #         currentSongTags['artwork'] = io.BytesIO(data).getvalue()
            #         # print(currentSongTags['artwork'])
            #     else:
            #         currentSongTags.append_tag('artwork', io.BytesIO(data).getvalue())
            #         # print(currentSongTags['artwork'])
            #     i += 1

        currentTrack.save()
#    return currentTrack
    
    def getTrackAlbum(self, track):
        if track['album'] is None:
            album = None
        else:
#           yt = getYouTubeAutorization()
            album=self.YouTubeAuth.get_album(track['album']['id'])
#         print(album)
        return album

    def downloadTrackFromYouTube(self, playlist,  track):
        album = self.getTrackAlbum(track)
        sYouTubeTrackURL = self.YouTubeURL + track['videoId']
        self.downloadAudioFromYouTube(sYouTubeTrackURL)
        sWorkingTrackFile = self.getNewestDownloadedFilename(self.WorkDirectory)
        self.setId3Tags(album, track, sWorkingTrackFile)
        # iDurationSeconds = track['duration_seconds']
        sTrackDirectory = self.getFileSystemDirectoryName(self.MusicRootDirectory, track)
        sTrackName = self.getFileSystemTrackName(album, track, self.Codec)
        if not os.path.exists(sTrackDirectory):
            os.makedirs(sTrackDirectory)
        os.rename(sWorkingTrackFile, os.path.join(sTrackDirectory, sTrackName))
#       return
     
 

