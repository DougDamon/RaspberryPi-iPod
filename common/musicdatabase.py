import os
#import pandas as pd
from datetime import datetime
from tinydb import TinyDB, Query,  where
from common.pipodconfiguration import piPodConfiguration

class MusicDB():
    def __init__(self):
        self.config = piPodConfiguration()
        self.HomeDirectory = self.config.HomeDirectory
        self.MusicDBLocation = self.config.MusicDBLocation
        self.MusicDBFile = self.config.MusicDBFile
        self.MusicDBFileLocation = self.config.MusicDBFileLocation
        self.YouTubeMusicSource = self.config.YouTubeDownloadSource
        self.db = self.getMusicDB()
        
    def getMusicDB(self):
#        dbFile = self.MusicDBLocation + self.MusicDBFile
        if os.path.isfile(self.MusicDBFileLocation) == False:
            open(self.MusicDBFileLocation, 'a')
        
        db = TinyDB(self.MusicDBFileLocation)
        return db
        
    def getTable(self,  TableName):
#        db = getDB()
        table = self.db.table(TableName)
        return table
     
#    def addYouTubeLibraryPlaylistsToDB(self, userPlaylists):
#        for pl in userPlaylists:
#            
#            self.addPlaylistToDB(pl, self.YouTubeMusicSource)
        
    def addPlaylistToDB(self,  Playlist,  Source):
        PlaylistQuery = Query()
        PlaylistTable = self.getTable('Playlist')
        sPlaylistId = Playlist ['id']
        sPlaylist = Playlist ['title']
        sDescription = Playlist['description']
        if Source == None:
            sSource = self.YouTubeMusicSource
        else:
            sSource = Source
        if len(PlaylistTable) > 0:
            QueryResult = PlaylistTable.search(where('PlaylistId') == sPlaylistId)
            if len(QueryResult) == 0 :
                PlaylistTable.insert({'PlaylistId' : sPlaylistId,  'Playlist' :  sPlaylist,  'Description' :  sDescription,  'Downloaded' : 'N',  'FlagForDownload' : 'N',  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            else:    
                PlaylistTable.update({'Playlist' :  sPlaylist,  'Description' :  sDescription,  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  PlaylistQuery.PlaylistTable.PlaylistId == sPlaylistId)
        else:
            PlaylistTable.insert({'PlaylistId' : sPlaylistId,  'Playlist' :  sPlaylist,  'Description' :  sDescription,  'Downloaded' : 'N',  'FlagForDownload' : 'N',  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})

    def addAlbumToDB(self,  AlbumId,  Album,  Source):
        AlbumQuery = Query()
        AlbumTable = self.getTable('Album')
        sAlbum = Album['title'] 
        sAlbumId = AlbumId
        sDescription = Album['description']
        sArtist = Album['artists'][0]['name']
        sArtistId = Album['artists'][0]['id']
        sYear = Album['year']
        sTrackCount = Album['trackCount']
        sDuration = Album['duration']
        if Source == None:
            sSource = self.YouTubeMusicSource
        else:
            sSource = Source
        
        AlbumQueryResult = AlbumTable.search(where('AlbumId ') == sAlbumId)
        if len(AlbumQueryResult) == 0 :
            AlbumTable.insert({'AlbumId ':  sAlbumId, 'Name' : sAlbum,  'Description' : sDescription, 'ArtistId' :  sArtistId, 'Artist' :  sArtist, 'Year' : sYear,  'TrackCount' :  sTrackCount, 'Duration' :  sDuration,  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:    
            AlbumTable.update({'Name' :  sAlbum,  'Description' : sDescription, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'Year' : sYear,  'TrackCount' :  sTrackCount, 'Duration' :  sDuration,  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  AlbumQuery.Album.AlbumId == sAlbumId )
    
    def addArtistToDB(self,  Playlist,  Album,  Track):
        artistQuery = Query()
        artistTable = self.getTable('Artist')
        sArtist = Track['artists'][0]['name']
        sArtistId = Track['artists'][0]['id']
        artistQueryResult = artistTable.search(where('ArtistId') == sArtistId)
    
        if len(artistQueryResult) == 0:
            artistTable.insert({'ArtistId' : sArtistId,  'ArtistName' :  sArtist, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:
            artistTable.update({'ArtistId' : sArtistId,  'ArtistName' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  artistQuery.Artist.ArtistId == sArtistId)
  
    def addTrackToDB(self, Playlist,  Album, Track, TrackPlaybackOrder,  FileLocation,  FileName,  Downloaded,  Source):
        trackQuery = Query()
        trackTable = self.getTable('Track')
        playlistTrackTable = self.getTable('PlaylistTrack')
    
        sPlaylistId = Playlist ['id']
        sPlaylist = Playlist ['title']
        sTrackId = Track['videoId']
        iTrackPlaybackOrder = TrackPlaybackOrder
        sTitle = Track['title']
        sArtist = Track['artists'][0]['name']
        sArtistId = Track['artists'][0]['id']
        # sDescription = Album['description']
        sAlbum = Album['title']
        sAlbumId = Track['album']['id']
        sTrackNumber = self.getAlbumTrackNumber(Album, Track)
        sFileLocation = FileLocation
        sFileName = FileName
        if Source == None:
            sSource = self.YouTubeMusicSource
        else:
            sSource = Source
    
        trackQueryResult = trackTable.search(where('TrackId') == sTrackId)
        playlistTrackQueryResult = playlistTrackTable.search((where('PlaylistId')  == sPlaylistId) & (where('TrackId')  == sTrackId))
    
        if len(trackQueryResult) == 0:
            trackTable.insert({'TrackId':  sTrackId, 'Title' : sTitle,  'FileLocation' : sFileLocation, 'FileName' : sFileName, 'AlbumId' : sAlbumId, 'Album' : sAlbum, 'TrackNumber' : sTrackNumber, 'ArtistId' :  sArtistId,'Artist' :  sArtist,  'Downloaded' : Downloaded,  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:
            trackTable.update({'Title' :  sTitle,  'FileLocation' : sFileLocation, 'FileName' : sFileName,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'TrackNumber' : sTrackNumber, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  trackQuery.Track.TrackId == sTrackId)
            
        if len(playlistTrackQueryResult) == 0:       
            playlistTrackTable.insert({'PlaylistId' : sPlaylistId, 'Playlist' :  sPlaylist, 'TrackId':  sTrackId, 'Title' : sTitle , 'TrackPlaybackOrder' : iTrackPlaybackOrder, 'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S") })
        else:    
            playlistTrackTable.update({'Playlist' :  sPlaylist, 'Title' : sTitle , 'TrackPlaybackOrder' :  iTrackPlaybackOrder, 'Source' :  sSource,  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S") },  trackQuery.Track.TrackId == sTrackId)


    def addSkippedTrackToDB(self, Playlist, SkippedTrack,  Source):
        skippedTrackQuery = Query()
        skippedTrackTable = self.getTable('SkippedTrack')
    
        sPlaylistId = Playlist ['id']
        sPlaylist = Playlist ['title']
        sSkippedTrackId = SkippedTrack['videoId']
        sTitle = SkippedTrack['title']
        sArtist = SkippedTrack['artists'][0]['name']
        sArtistId = SkippedTrack['artists'][0]['id']
    # sDescription = Album['description']
        sAlbum = SkippedTrack['name']
        sAlbumId = SkippedTrack['album']['id']
    
        if Source == None:
            sSource = self.YouTubeMusicSource
        else:
            sSource = Source
    
        skippedTrackQueryResult = skippedTrackTable.search(where('TrackId') == sSkippedTrackId)
    
        if len(skippedTrackQueryResult) == 0:
            skippedTrackTable.insert({'TrackId':  sSkippedTrackId, 'Title' : sTitle,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'PlaylistId' : sPlaylistId, 'Playlist' :  sPlaylist,   'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:
            skippedTrackTable.update({'Title' :  sTitle,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  skippedTrackQuery.SkippedTrack.TrackId == sSkippedTrackId)
     
    def removeAlbumFromDB(self, AlbumId):
        sAlbumId = AlbumId
        albumTable = self.getTable('Album')
        albumQuery = Query()
        if 'Album' in self.db.tables():
            albumTable.remove(albumQuery.AlbumId == sAlbumId)
    
    def removePlaylistFromDB(self,  PlaylistId):
        sPlaylistId = PlaylistId
        self.removePlaylistTracksFromDB(sPlaylistId)
        playlistTable = self.getTable('Playlist')
        playlistQuery = Query()
        if 'Playlist' in self.db.tables():
            playlistTable.remove(playlistQuery.PlaylistId == sPlaylistId)
            
    def removePlaylistTracksFromDB(self, PlaylistId):
        sPlaylistId = PlaylistId
        playlistTrackTable = self.getTable('PlaylistTrack')
        playlistTrackQuery = Query()
        if 'PlaylistTrack' in self.db.tables():
            playlistTrackTable.remove(playlistTrackQuery.PlaylistId == sPlaylistId)

    def getAlbumFromDB(self, albumId):
        albumTable = self.getTable('Album')
        album = albumTable.search(where('AlbumId') == albumId )
        return album
    
    def getPlaylistsFromDB(self):
        playlists =  self.getTable('Playlist')
        return  playlists
    
    def getPlaylistsForDownload(self):
        playlistTable = self.getTable('Playlist')
        playlists = playlistTable.search(where('FlagForDownload') == 'Y' )
        return playlists

    def getDownloadedPlaylists(self):
        playlistTable = self.getTable('Playlist')
        playlists = playlistTable.search(where('Downloaded') == 'Y' )
        return playlists
        
    def getTrackFromDB(self,  TrackId):
        sTrackId = TrackId
        trackTable = self.getTable('Track')
        track = trackTable.search(where('TrackId') == sTrackId)
        if isinstance(track,  list):
            track = track[0]
        return track
        
    def getPlaylistTracksFromDB(self, currentPlaylistId):
        trackTable = self.getTable('PlaylistTrack')
        playlistTracks = trackTable.search(where('PlaylistId') == currentPlaylistId)
        playlistTracks = sorted(playlistTracks, key=lambda x: x['TrackPlaybackOrder'], reverse=False)
        return playlistTracks
    
    def  setPlaylistDownloaded(self, DownloadedPlaylistId):
        playlistQuery = Query()
        playlistTable = self.getTable('Playlist')
        playlistTable.update({'Downloaded' : 'Y', 'FlagForDownload' : 'N', 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  playlistQuery.PlaylistId == DownloadedPlaylistId)
    
    def resetMusicDB(self):
        self.db.drop_tables()
        self.db.truncate()
    
    def  resetPlaylistDownloaded(self, DownloadedPlaylistId):
        playlistQuery = Query()
        playlistTable = self.getTable('Playlist')
        playlistTable.update({'Downloaded' : 'N', 'FlagForDownload' : 'N', 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  playlistQuery.PlaylistId == DownloadedPlaylistId)
    
    def  setPlaylistForDownload(self, DownloadPlaylistId): 
        PlaylistTable = self.getTable('Playlist')
        PlaylistQuery = Query()
        PlaylistTable.update({'FlagForDownload' : 'Y','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  PlaylistQuery.PlaylistId == DownloadPlaylistId) 
        
    def  resetPlaylistForDownload(self, DownloadPlaylistId): 
        PlaylistTable = self.getTable('Playlist')
        PlaylistQuery = Query()
        PlaylistTable.update({'FlagForDownload' : 'N','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  PlaylistQuery.PlaylistId == DownloadPlaylistId)     
    
    def getAlbumTrackNumber(self,  Album, Track):
        # ytAlbum = YouTubeConnection.get_album(YouTubeSong['album']['id'])
        # print(YouTubeAlbum)
        if Album is None:
            trackNumber = '00'
        else:
            i = 1
            for albumTrack in Album['tracks']:
                if albumTrack['videoId'] == Track['videoId']:
                    if len(str(i)) == 1:
                        trackNumber = '0' + str(i)
                    else:
                        trackNumber = str(i)
            i += 1
        return trackNumber

    def clearNowPlayingPlaylist(self):
        nowPlayingPlaylistTable = self.getTable('nowPlayingPlaylistTable')
        nowPlayingPlaylistTable.truncate()
        self.clearNowPlayingTrack()
    
    def clearNowPlayingTrack(self):
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        nowPlayingTrackTable.truncate()
        
    def getNowPlayingPlaylist(self):
        nowPlayingPlaylistTable =  self.getTable('nowPlayingPlaylistTable')
        return  nowPlayingPlaylistTable
        
    def getNowPlayingTrack(self):
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        return nowPlayingTrackTable
    
    def addPlaylistToNowPlaying(self,  PlaylistTracks):
        lPlaylistTracks = PlaylistTracks
        nowPlayingPlaylistTable =  self.getTable('NowPlayingPlaylist')
        nowPlayingPlaylistTable.insert_multiple(lPlaylistTracks)
    
    def setNowPlayingTrack(self,  TrackId,  Duration,  InitialPosition = 0,  CurrentPosition = 0):
        sTrackId = TrackId
        fInitialPosition = InitialPosition
        fCurrentPosition = CurrentPosition
        fDuration = Duration
        nowPlayingPlaylistTable =  self.getTable('NowPlayingPlaylist')
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        nowPlayingQuery = Query()
        nowPlayingPlaylistTable.update({'NowPlaying' : 'N','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  nowPlayingQuery.NowPlaying == 'Y')
        nowPlayingPlaylistTable.update({'NowPlaying' : 'Y','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  nowPlayingQuery.TrackId == sTrackId)
        self.clearNowPlayingTrack()
        nowPlayingTrackTable.insert({'Trackid' : sTrackId,  'Duration' : fDuration,  'InitialPosition' : fInitialPosition,  'CurrentPosition' : fCurrentPosition})
        
    def updateNowPlayingTrack(self, TrackId,  CurrentPosition):
        sTrackId = TrackId
        fCurrentPosition = CurrentPosition
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        nowPlayingQuery = Query()
        nowPlayingTrackTable.update({'CurrentPosition' : fCurrentPosition},  nowPlayingQuery.TrackId == sTrackId)
        
        
        
        
        
        
    
        
