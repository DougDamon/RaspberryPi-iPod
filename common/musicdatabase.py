import os
from datetime import datetime

import pandas as pd
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
        
        self.dfEmpty = pd.DataFrame()
        if len(self.getTable('NowPlayingPlaylist')) > 0 and len(self.getTable('NowPlayingTrack')) >= 0:
            dfNowPlayingPlaylist = self.getCurrentPlaylist()
            dfNowPlayingTrack = self.getCurrentTrack()
            self.NowPlayingPlaylistId = dfNowPlayingPlaylist.iloc[0]['PlaylistId']
            self.NowPlayingTrackId = dfNowPlayingTrack.iloc[0]['TrackId']
            self.CurrentPlaylistInfo = self.getPlaylistInfoFromDB(self.NowPlayingPlaylistId)
        else:
            self.NowPlayingPlaylistId = None
            self.NowPlayingTrackId = None
            self.CurrentPlaylistInfo = None
        
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
        iDurationSeconds = Track['duration_seconds']
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
            trackTable.insert({'TrackId':  sTrackId, 'Title' : sTitle,  'DurationSeconds' : iDurationSeconds, 'FileLocation' : sFileLocation, 'FileName' : sFileName, 'AlbumId' : sAlbumId, 'Album' : sAlbum, 'TrackNumber' : sTrackNumber, 'ArtistId' :  sArtistId,'Artist' :  sArtist,  'Downloaded' : Downloaded,  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        else:
            trackTable.update({'Title' :  sTitle, 'DurationSeconds' : iDurationSeconds,  'FileLocation' : sFileLocation, 'FileName' : sFileName,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'TrackNumber' : sTrackNumber, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  trackQuery.Track.TrackId == sTrackId)
            
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
        albumQuery= Query()
        album = albumTable.get(albumQuery.AlbumId == albumId)
#        album = albumTable.search(where('AlbumId') == albumId )
        dfAlbum = pd.DataFrame(album)
        return dfAlbum
    
    def getPlaylistIdbyNamefromDB(self, PlaylistName):
        sPlaylistName = PlaylistName
        playlistTable = self.getTable('Playlist')
        playlist = playlistTable.search(where('Playlist') == sPlaylistName )
        sPlaylistId = playlist[0]['PlaylistId']
        return sPlaylistId
        
    def getTrackIdByNameFromDB(self,  PlaylistId,  TrackName):
        sPlaylistId = PlaylistId
        sTitle = TrackName
        trackQuery = Query()
        playlistTrackTable = self.getTable('PlaylistTrack')
#        track = playlistTrackTable.search(where((('PlaylistId') == sPlaylistId) & (('Title')  == sTrackName))) #[0]
        track = playlistTrackTable.search((trackQuery.PlaylistId == sPlaylistId) & (trackQuery.Title  == sTitle))[0]
        sTrackId = track['TrackId']
        return sTrackId
        
    def getPlaylistsFromDB(self):
        playlists =  self.getTable('Playlist')
        dfPlaylists = pd.DataFrame(playlists)
        return  dfPlaylists
        
    def getPlaylistInfoFromDB(self,  PlaylistId):
        sPlaylistId = PlaylistId
        playlistTable = self.getTable('Playlist')
        playlist = playlistTable.search(where('PlaylistId') == sPlaylistId )
        playlistTracks = self.getPlaylistTracksFromDB(sPlaylistId)
        sTrackCount = str(playlistTracks.shape[0])
        dfPlaylistInfo = pd.DataFrame(playlist)
        dfPlaylistInfo['TrackCount'] = sTrackCount
        return dfPlaylistInfo
        
    
    def getPlaylistsForDownload(self):
        playlistTable = self.getTable('Playlist')
        playlists = playlistTable.search(where('FlagForDownload') == 'Y' )
        return playlists

    def getDownloadedPlaylists(self):
        playlistTable = self.getTable('Playlist')
        playlists = playlistTable.search(where('Downloaded') == 'Y' )
        dfPlaylists = pd.DataFrame(playlists)
        return dfPlaylists
        
    def getTrackFromDB(self,  TrackId):
        sTrackId = TrackId
        trackTable = self.getTable('Track')
        track = trackTable.search(where('TrackId') == sTrackId)
#        if isinstance(track,  list):
#            track = track[0]
        dfTrack = pd.DataFrame(track) 
        return dfTrack
        
    def getTrackTableFromDB(self):    
        tracks =  self.getTable('Track')
        dfTracks = pd.DataFrame(tracks)
        return dfTracks
        
    def getPlaylistTracksFromDB(self, currentPlaylistId):
        sCurrentPlaylistId = currentPlaylistId
        trackTable = self.getTable('PlaylistTrack')
        playlistTracks = trackTable.search(where('PlaylistId') == sCurrentPlaylistId)
#        playlistTracks = sorted(playlistTracks, key=lambda x: x['TrackPlaybackOrder'], reverse=False)
        dfPlaylistTracks = pd.DataFrame(playlistTracks)
        dfPlaylistTracks = dfPlaylistTracks.sort_values('TrackPlaybackOrder')
        dfPlaylistTracks = dfPlaylistTracks.reset_index(drop=True)
        return dfPlaylistTracks
    
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

    def clearCurrentPlaylist(self):
        nowPlayingPlaylistTable = self.getTable('NowPlayingPlaylist')
        nowPlayingPlaylistTable.truncate()
        self.clearCurrentTrack()
    
    def clearCurrentTrack(self):
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        nowPlayingTrackTable.truncate()
     
    def getCurrentPlaylist(self):
        nowPlayingPlaylistTable =  self.getTable('NowPlayingPlaylist')
        dfNowPlayingPlaylist = pd.DataFrame(nowPlayingPlaylistTable)
        if dfNowPlayingPlaylist.shape[0] == 0:
            return self.dfEmpty
        else:
            return  dfNowPlayingPlaylist.sort_values('CurrentPlaybackOrder')
    
    def getCurrentPlaylistInfo(self):
        return self.CurrentPlaylistInfo
    
    def getFirstTrack(self,  PlaylistId):
        dfPlaylistTracks = self.getPlaylistTracksFromDB(PlaylistId)
        if dfPlaylistTracks.shape[0]==0:
            return self.dfEmpty
        else:
            return self.getTrackFromDB(dfPlaylistTracks.iloc[0]['TrackId'])
        
    def getCurrentTrack(self):
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        dfNowPlayingPlaylist = self.getCurrentPlaylist()
        dfNowPlayingTrack = pd.DataFrame(nowPlayingTrackTable)
        if dfNowPlayingTrack.shape[0] == 0 and dfNowPlayingPlaylist.shape[0] == 0:
            return self.dfEmpty
        elif dfNowPlayingTrack.shape[0] == 0 and dfNowPlayingPlaylist.shape[0] >=1:
            dfFirstTrack = self.getFirstTrack(dfNowPlayingPlaylist.iloc[0]['PlaylistId'])
            self.setCurrentTrack(dfFirstTrack.iloc[0]['TrackId'],  dfNowPlayingPlaylist.iloc[0]['PlaylistId'])
            return dfFirstTrack
        else:
            return dfNowPlayingTrack
    
    def getNextTrack(self):
        CurrentTrackIndex = None
        dfNowPlayingTrack = self.getCurrentTrack()
        dfNowPlayingPlaylist = self.getCurrentPlaylist()
        sNowPlayingTrackId = dfNowPlayingTrack.iloc[0]['TrackId']
        CurrentTrackIndex= dfNowPlayingPlaylist.index.get_loc(dfNowPlayingPlaylist.loc[(dfNowPlayingPlaylist['NowPlaying'] == 'Y') & (dfNowPlayingPlaylist['TrackId'] ==  sNowPlayingTrackId)].index[0])
#        print('max index:',  dfNowPlayingPlaylist.shape[0]-1)
        if CurrentTrackIndex != None and CurrentTrackIndex < dfNowPlayingPlaylist.shape[0] - 1:
            dfNextTrack = dfNowPlayingPlaylist.iloc[[CurrentTrackIndex+1]]
            dfNextTrack.reset_index(drop=True, inplace=True)
        else:
            dfNextTrack = self.dfEmpty
        return dfNextTrack
        
    def getPreviousTrack(self):
        CurrentTrackIndex = None
        dfNowPlayingTrack = self.getCurrentTrack()
        dfNowPlayingPlaylist = self.getCurrentPlaylist()
        sNowPlayingTrackId = dfNowPlayingTrack.iloc[0]['TrackId']
        CurrentTrackIndex= dfNowPlayingPlaylist.index.get_loc(dfNowPlayingPlaylist.loc[(dfNowPlayingPlaylist['NowPlaying'] == 'Y') & (dfNowPlayingPlaylist['TrackId'] ==  sNowPlayingTrackId)].index[0])
        if CurrentTrackIndex >= 1:
            dfPreviousTrack = dfNowPlayingPlaylist.iloc[[CurrentTrackIndex-1]]
            dfPreviousTrack.reset_index(drop=True, inplace=True)
        else:
            dfPreviousTrack = self.dfEmpty
        return dfPreviousTrack

    def getNextPlaylistIdTrackId(self):
        dfNextPlaylistTrack = self.getNextTrack()
        if len(dfNextPlaylistTrack) == 1:
            NextPlaylistId = dfNextPlaylistTrack['PlaylistId'][0]
            NextTrackId = dfNextPlaylistTrack['TrackId'][0] 
        else:
            NextPlaylistId = None
            NextTrackId = None
        return NextPlaylistId,  NextTrackId
        
    def getPreviousPlaylistIdTrackId(self):
        dfPreviousPlaylistTrack = self.getPreviousTrack()
        if len(dfPreviousPlaylistTrack) == 1:
            PreviousPlaylistId = dfPreviousPlaylistTrack['PlaylistId'][0]
            PreviousTrackId = dfPreviousPlaylistTrack['TrackId'][0] 
        else:
            PreviousPlaylistId = None
            PreviousTrackId = None
        return PreviousPlaylistId,  PreviousTrackId
        
    def getSelectedPlaylistTracksFromDB(self,  PlaylistId):
#        get playlist from db
        sPlaylistId = PlaylistId
        duplicateTrackColumns = ['Title', 'Source',  'CreateDate',  'LastUpdateDate']
        dfPlaylistTracks = self.getPlaylistTracksFromDB(sPlaylistId)
        dfTracks = self.getTrackTableFromDB()
        dfTracks.drop(duplicateTrackColumns, axis=1,  inplace=True)
        dfNowPlayingTracks = dfPlaylistTracks.merge(dfTracks, on='TrackId', how='inner')
        dfNowPlayingTracks['CurrentPlaybackOrder'] = dfNowPlayingTracks['TrackPlaybackOrder']
        dfNowPlayingTracks['NowPlaying'] = 'N'
        dfNowPlayingTracks['CreateDate'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        dfNowPlayingTracks['LastUpdateDate'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return dfNowPlayingTracks

    
    def addCurrentPlaylistToDB(self,  PlaylistId):
        sPlaylistId = PlaylistId
        dfNowPlayingPlaylistTracks = self.getSelectedPlaylistTracksFromDB(sPlaylistId)
        nowPlayingPlaylistTable =  self.getTable('NowPlayingPlaylist')
        nowPlayingPlaylistTable.insert_multiple(dfNowPlayingPlaylistTracks.to_dict(orient='records'))
 
    def setCurrentTrack(self,  TrackId,  Duration = 0, InitialPosition = 0,  CurrentPosition = 0):
        sTrackId = TrackId
        fDuration = Duration
        fInitialPosition = InitialPosition
        fCurrentPosition = CurrentPosition

        nowPlayingPlaylistTable =  self.getTable('NowPlayingPlaylist')
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        nowPlayingQuery = Query()
        nowPlayingPlaylistTable.update({'NowPlaying' : 'N','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  nowPlayingQuery.NowPlaying == 'Y')
        nowPlayingPlaylistTable.update({'NowPlaying' : 'Y','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  nowPlayingQuery.TrackId == sTrackId)
        self.clearCurrentTrack()
        nowPlayingTrackTable.insert({'TrackId' : sTrackId,  'DurationSeconds' : fDuration, 'InitialPosition' : fInitialPosition,  'CurrentPosition' : fCurrentPosition})
 
    def setCurrentPlaylist(self,  PlaylistId):
#        sPlaylistId =  PlaylistId
#        sTrackId = TrackId
#        if sPlaylistId != self.NowPlayingPlaylistId:
#        self.clearNowPlayingTrack()
        self.clearCurrentPlaylist()
        self.addCurrentPlaylistToDB(PlaylistId)
        self.CurrentPlaylistInfo = self.getPlaylistInfoFromDB(PlaylistId)
        self.NowPlayingPlaylistId = PlaylistId
#            self.setNowPlayingTrack(sTrackId)  
#        elif sPlaylistId == self.NowPlayingPlaylistId and sTrackId != self.NowPlayingTrackId:
#            self.setNowPlayingTrack(sTrackId)
        return  self.CurrentPlaylistInfo
        
    def updateCurrentTrack(self, TrackId,  CurrentPosition):
        sTrackId = TrackId
        fCurrentPosition = CurrentPosition
        nowPlayingTrackTable = self.getTable('NowPlayingTrack')
        nowPlayingQuery = Query()
        nowPlayingTrackTable.update({'CurrentPosition' : fCurrentPosition},  nowPlayingQuery.TrackId == sTrackId)
        
        
    def getCurrentPlaylistId(self):
        dfNowPlayingPlaylist = self.getCurrentPlaylist()
        if dfNowPlayingPlaylist.shape[0] == 0:
            return None
        else:
            return dfNowPlayingPlaylist['PlaylistId'][0]
    
    def getCurrentTrackId(self):
        dfCurrentTrack = self.getCurrentTrack()
        if dfCurrentTrack.shape[0] == 0:
            return None
        else:
            return dfCurrentTrack['TrackId'][0]
            
    def setCurrentPlaybackOrder(self, TrackId,  PlaybackOrder):
        sTrackId = TrackId
        fPlaybackOrder = PlaybackOrder
        nowPlayingPlaylistTable =  self.getTable('NowPlayingPlaylist')
        nowPlaybackOrderQuery = Query()
        nowPlayingPlaylistTable.update({'CurrentPlaybackOrder' : fPlaybackOrder},  nowPlaybackOrderQuery.TrackId == sTrackId)

    def shuffleCurrentPlaylist(self):
        iTrackOrder = 1
        # get current playlist into a dataframe
        sCurrentPlaylistId = self.getCurrentPlaylistId()
        if sCurrentPlaylistId == None:
            print('No current playlist')
            return
        # get current playlist tracks
        dfCurrentPlaylistTracks = self.getCurrentPlaylist()
        # get the currently playing track
        CurrentTrackId = self.getCurrentTrackId()
        # if no track, set first Track in playlist to current Track
        if CurrentTrackId == None:
            self.setCurrentTrack(self.getFirstTrack(sCurrentPlaylistId))
            CurrentTrackId = self.getCurrentTrackId()
        # move current track to its own dataframe
#        dfCurrentTrack = dfCurrentPlaylistTracks.loc[dfCurrentPlaylistTracks['TrackId'] == CurrentTrackId]
        dfRemainingTracks = dfCurrentPlaylistTracks.loc[dfCurrentPlaylistTracks['TrackId'] != CurrentTrackId]
        # randomly reorder the playlist
        dfShuffleList = dfRemainingTracks.sample(frac=1)
        # merge the first track dataframe and the 
        self.setCurrentPlaybackOrder(CurrentTrackId,  iTrackOrder)
        
        for Index,  Track in dfShuffleList.iterrows():
            iTrackOrder += 1
            self.setCurrentPlaybackOrder(Track['TrackId'],  iTrackOrder)
        
        return
    
    def unshuffleCurrentPlaylist(self):
        dfCurrentPlaylistTracks = self.getCurrentPlaylist()
        
        for Index, Track in dfCurrentPlaylistTracks.iterrows():
            self.setCurrentPlaybackOrder(Track['TrackId'],  Track['TrackPlaybackOrder'])
        
        
