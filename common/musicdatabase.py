import os
from datetime import datetime
from tinydb import TinyDB, Query
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
     
    def addYouTubeLibraryPlaylistsToDB(self, userPlaylists):
        for pl in userPlaylists:
            self.addPlaylistToDB(pl, self.YouTubeMusicSource)
        
    def addPlaylistToDB(self,  Playlist,  Source):
        PlaylistQuery = Query()
        PlaylistTable = self.getTable('Playlist')
        sPlaylistId = Playlist ['playlistId']
        sPlaylist = Playlist ['title']
        sDescription = Playlist['description']
        if Source == None:
            sSource = self.YouTubeMusicSource
        else:
            sSource = Source
        if len(PlaylistTable) > 0:
            QueryResult = PlaylistTable.search(PlaylistQuery.PlaylistId == Playlist ['playlistId'])
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
        
        AlbumQueryResult = AlbumTable.search(AlbumQuery.Album.AlbumId == sAlbumId)
        if len(AlbumQueryResult) == 0 :
            AlbumTable.insert({'AlbumId ':  sAlbumId, 'Name' : sAlbum,  'Description' : sDescription, 'ArtistId' :  sArtistId, 'Artist' :  sArtist, 'Year' : sYear,  'TrackCount' :  sTrackCount, 'Duration' :  sDuration,  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:    
            AlbumTable.update({'Name' :  sAlbum,  'Description' : sDescription, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'Year' : sYear,  'TrackCount' :  sTrackCount, 'Duration' :  sDuration,  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  AlbumQuery.Album.AlbumId == sAlbumId )
    
    def addArtistToDB(self,  Playlist,  Album,  Track):
        artistQuery = Query()
        artistTable = self.getTable('Artist')
        sArtist = Track['artists'][0]['name']
        sArtistId = Track['artists'][0]['id']
        artistQueryResult = artistTable.search(artistQuery.artistTable.ArtistId == sArtistId)
    
        if len(artistQueryResult) == 0:
            artistTable.insert({'ArtistId' : sArtistId,  'ArtistName' :  sArtist, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:
            artistTable.update({'ArtistId' : sArtistId,  'ArtistName' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  artistQuery.Artist.ArtistId == sArtistId)
  
    def addTrackToDB(self, Playlist,  Album, Track, TrackPlaybackOrder,  FileLocation,  FileName,  Downloaded,  Source):
        trackQuery = Query()
        playlistTrackQuery = Query()
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
    
        trackQueryResult = trackTable.search(trackQuery.Track.TrackId == sTrackId)
        playlistTrackQueryResult = playlistTrackTable.search((playlistTrackQuery.playlistTrack.PlaylistId == sPlaylistId) & (playlistTrackQuery.PlaylistTrack.TrackId == sTrackId))
    
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
    
        skippedTrackQueryResult = skippedTrackTable.search(skippedTrackQuery.SkippedTrack.TrackId == sSkippedTrackId)
    
        if len(skippedTrackQueryResult) == 0:
            skippedTrackTable.insert({'TrackId':  sSkippedTrackId, 'Title' : sTitle,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'PlaylistId' : sPlaylistId, 'Playlist' :  sPlaylist,   'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:
            skippedTrackTable.update({'Title' :  sTitle,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  skippedTrackQuery.SkippedTrack.TrackId == sSkippedTrackId)
     
    
    def removePlaylistTracksFromDB(self, PlaylistId):
        sPlaylistId = PlaylistId
        playlistTrackTable = self.getTable('PlaylistTrack')
        playlistTrackQuery = Query()
        if 'PlaylistTrack' in self.db.tables():
            playlistTrackTable.remove(playlistTrackQuery.playlistTrackTable.PlaylistId == sPlaylistId)

    def getAlbumFromDB(self, albumId):
        albumTable = self.getTable('Album')
        albumQuery = Query()
        album = albumTable.search(albumQuery.albumTable.AlbumId == albumId )
        return album
    
    def getPlaylistsFromDB(self):
        playlists =  self.getTable('Playlist')
        return  playlists
    
    def getPlaylistsForDownload(self):
        playlistTable = self.getTable('Playlist')
        playlistQuery = Query()
        playlists = playlistTable.search(playlistQuery.FlagForDownload == 'Y' )
        return playlists

    def getDownloadedPlaylists(self):
        playlistTable = self.getTable('Playlist')
        playlistQuery = Query()
        playlists = playlistTable.search(playlistQuery.Downloaded == 'Y' )
        return playlists
 
    def getPlaylistTracksFromDB(self, currentPlaylistId):
        trackTable = self.getTable('Track')
        trackQuery = Query()
        queryResult = trackTable.search(trackQuery.PlaylistId == currentPlaylistId)
        return queryResult
    
    def  setPlaylistDownloaded(self, DownloadedPlaylistId):
        playlistQuery = Query()
        playlistTable = self.getTable('Playlist')
        playlistTable.update({'Downloaded' : 'Y', 'FlagForDownload' : 'N', 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  playlistQuery.PlaylistId == DownloadedPlaylistId)
    
    def  setPlaylistForDownload(self, DownloadPlaylistId): 
        PlaylistTable = self.getTable('Playlist')
        PlaylistQuery = Query()
        PlaylistTable.update({'FlagForDownload' : 'Y','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  PlaylistQuery.PlaylistId == DownloadPlaylistId) 
    
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
