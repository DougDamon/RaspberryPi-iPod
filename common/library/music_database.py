import os
import uuid
from datetime import datetime

import pandas as pd
from tinydb import TinyDB, Query,  where
from common.config.settings import ConfigService

class MusicDB():
    def __init__(self):
        self.config = ConfigService()
        self.HomeDirectory = self.config.HomeDirectory
        self.MusicDBLocation = self.config.MusicDBLocation
        self.MusicDBFile = self.config.MusicDBFile
        self.MusicDBFileLocation = self.config.MusicDBFileLocation
        self.YouTubeMusicSource = self.config.YouTubeDownloadSource
        self.db = self.getMusicDB()
        
        self.dfEmpty = pd.DataFrame()
        if len(self.getTable('NowPlayingPlaylist')) > 0:
            dfCurrentPlaylist = self.getCurrentPlaylist()
            dfCurrentTrack = self.getCurrentTrack()
        
            self.CurrentPlaylistId = dfCurrentPlaylist.iloc[0]['PlaylistId']
            self.CurrentTrackId = dfCurrentTrack.iloc[0]['TrackId']
        
            self.CurrentPlaylistInfo = pd.DataFrame([
                {
                    'PlaylistId': self.CurrentPlaylistId,
                    'Playlist': dfCurrentPlaylist.iloc[0]['Playlist'],
                    'TrackCount': len(dfCurrentPlaylist)
                }
            ])
        else:
            self.CurrentPlaylistId = None
            self.CurrentTrackId = None
            self.CurrentPlaylistInfo = None
        
#        self.CurrentPlaylistId = self.getCurrentPlaylistId()
#        self.CurrentPlaylistInfo = self.getCurrentPlaylistInfo()
#            
#        self.CurrentTrackId = self.getCurrentTrackId()
#        print(self.CurrentPlaylistId,  self.CurrentTrackId)
        self.NextPlaylistId = None
        self.NextTrackId = None
        
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

    def getOrCreateImportedArtist(self, artist_name):
        artist_table = self.getTable('Artist')
    
        artist = artist_table.search(
            where('ArtistName') == artist_name
        )
    
        if len(artist) > 0:
            return artist[0]['ArtistId']
    
        artist_id = str(uuid.uuid4())
    
        artist_table.insert({
            'ArtistId': artist_id,
            'ArtistName': artist_name,
            'CreateDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'LastUpdateDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })
    
        return artist_id
    
    def getOrCreateImportedAlbum(self, artist_id, artist_name, album_name):
        album_table = self.getTable('Album')
    
        album = album_table.search(
            (where('ArtistId') == artist_id) &
            (where('Name') == album_name)
        )
    
        if len(album) > 0:
            return album[0]['AlbumId']
    
        album_id = str(uuid.uuid4())
    
        album_table.insert({
            'AlbumId': album_id,
            'Name': album_name,
            'ArtistId': artist_id,
            'Artist': artist_name,
            'Source': 'FileImport',
            'CreateDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'LastUpdateDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })

        return album_id
    
    def addImportedTrackToDB(
        self,
        title,
        artist,
        album,
        track_number,
        genre,
        duration_seconds,
        file_location,
        file_name,
        source="FileImport"
    ):
        track_table = self.getTable('Track')

        artist_id = self.getOrCreateImportedArtist(artist)
        
        album_id = self.getOrCreateImportedAlbum(
            artist_id,
            artist,
            album
        )
        
        track_id = str(uuid.uuid4())
    
        track_table.insert({
            'TrackId': track_id,
            'Title': title,
            'DurationSeconds': duration_seconds,
            'FileLocation': file_location,
            'FileName': file_name,
            'AlbumId': album_id,
            'Album': album,
            'TrackNumber': track_number,
            'ArtistId': artist_id,
            'Artist': artist,
            'Genre': genre,
            'Downloaded': 'Y',
            'Source': source,
            'CreateDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'LastUpdateDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })
    
        return track_id

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

    def getArtistsFromDB(self):
        tracks = self.getTrackTableFromDB()
    
        if tracks.empty or 'Artist' not in tracks.columns:
            return pd.DataFrame(columns=['Artist'])
    
        artists = tracks[['Artist']].dropna()
        artists = artists[artists['Artist'].str.strip() != '']
        artists = artists.drop_duplicates()
        artists = artists.sort_values('Artist', key=lambda x: x.str.lower())
        artists = artists.reset_index(drop=True)
    
        return artists
    
    
    def getAlbumsFromDB(self):
        tracks = self.getTrackTableFromDB()
    
        if tracks.empty or 'Album' not in tracks.columns:
            return pd.DataFrame(columns=['Album'])
    
        albums = tracks[['Album']].dropna()
        albums = albums[albums['Album'].str.strip() != '']
        albums = albums.drop_duplicates()
        albums = albums.sort_values('Album', key=lambda x: x.str.lower())
        albums = albums.reset_index(drop=True)
    
        return albums
    
    
    def getGenresFromDB(self):
        tracks = self.getTrackTableFromDB()
    
        if tracks.empty or 'Genre' not in tracks.columns:
            return pd.DataFrame(columns=['Genre'])
    
        genres = tracks[['Genre']].dropna()
        genres = genres[genres['Genre'].str.strip() != '']
        genres = genres.drop_duplicates()
        genres = genres.sort_values('Genre', key=lambda x: x.str.lower())
        genres = genres.reset_index(drop=True)
    
        return genres
    
    def getTracksByArtistFromDB(self, artist):
        tracks = self.getTrackTableFromDB()
    
        if tracks.empty or 'Artist' not in tracks.columns:
            return pd.DataFrame()
    
        tracks = tracks[tracks['Artist'] == artist].copy()
    
        if tracks.empty:
            return tracks
    
        tracks = self.sortTracksForDisplay(tracks)
    
        return tracks
    
    
    def getTracksByAlbumFromDB(self, album):
        tracks = self.getTrackTableFromDB()
    
        if tracks.empty or 'Album' not in tracks.columns:
            return pd.DataFrame()
    
        tracks = tracks[tracks['Album'] == album].copy()
    
        if tracks.empty:
            return tracks
    
        tracks = self.sortTracksForDisplay(tracks)
    
        return tracks
    
    
    def getTracksByGenreFromDB(self, genre):
        tracks = self.getTrackTableFromDB()
    
        if tracks.empty or 'Genre' not in tracks.columns:
            return pd.DataFrame()
    
        tracks = tracks[tracks['Genre'] == genre].copy()
    
        if tracks.empty:
            return tracks
    
        tracks = self.sortTracksForDisplay(tracks)
    
        return tracks
    
    def sortTracksForDisplay(self, tracks):
        tracks = tracks.copy()
    
        if 'TrackNumber' not in tracks.columns:
            return tracks.sort_values(
                'Title',
                key=lambda x: x.str.lower()
            ).reset_index(drop=True)
    
        tracks['TrackNumberSort'] = pd.to_numeric(
            tracks['TrackNumber'],
            errors='coerce'
        )
    
        tracks['HasTrackNumber'] = tracks['TrackNumberSort'].notna()
    
        tracks = tracks.sort_values(
            by=[
                'HasTrackNumber',
                'TrackNumberSort',
                'Title'
            ],
            ascending=[
                False,
                True,
                True
            ],
            key=lambda column: (
                column.str.lower()
                if column.name == 'Title'
                else column
            )
        )
    
        tracks = tracks.drop(
            columns=[
                'TrackNumberSort',
                'HasTrackNumber'
            ]
        )
    
        tracks = tracks.reset_index(drop=True)
    
        return tracks
    
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
    
    def getTrackIdFromCurrentPlaylistByTitle(self, title):
        dfCurrentPlaylist = self.getCurrentPlaylist()
    
        if dfCurrentPlaylist.empty:
            return None
    
        matches = dfCurrentPlaylist[
            dfCurrentPlaylist['Title'] == title
        ]

        if matches.empty:
            return None
    
        return matches.iloc[0]['TrackId']
    
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
    
        if dfNowPlayingTrack.shape[0] > 0:
            return dfNowPlayingTrack
    
        if dfNowPlayingPlaylist.shape[0] == 0:
            return self.dfEmpty
    
        first_track_id = dfNowPlayingPlaylist.iloc[0]['TrackId']
    
        dfFirstTrack = self.getTrackFromDB(
            first_track_id
        )
    
        if dfFirstTrack.empty:
            return self.dfEmpty
    
        duration = int(dfFirstTrack.iloc[0]['DurationSeconds'])
    
        self.setCurrentTrack(
            first_track_id,
            duration,
            0,
            0
        )
    
        return dfFirstTrack
    
    def getNextTrack(self):
        CurrentTrackIndex = None
        dfNowPlayingTrack = self.getCurrentTrack()
        dfNowPlayingPlaylist = self.getCurrentPlaylist()
        sCurrentTrackId = dfNowPlayingTrack.iloc[0]['TrackId']
        CurrentTrackIndex= dfNowPlayingPlaylist.index.get_loc(dfNowPlayingPlaylist.loc[(dfNowPlayingPlaylist['NowPlaying'] == 'Y') & (dfNowPlayingPlaylist['TrackId'] ==  sCurrentTrackId)].index[0])
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
        sCurrentTrackId = dfNowPlayingTrack.iloc[0]['TrackId']
        CurrentTrackIndex= dfNowPlayingPlaylist.index.get_loc(dfNowPlayingPlaylist.loc[(dfNowPlayingPlaylist['NowPlaying'] == 'Y') & (dfNowPlayingPlaylist['TrackId'] ==  sCurrentTrackId)].index[0])
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
 
    def setCurrentTrackList(self, dfTracks, queue_id, queue_name):
        self.clearCurrentPlaylist()
    
        now_playing_table = self.getTable('NowPlayingPlaylist')
    
        records = []
    
        for index, row in dfTracks.reset_index(drop=True).iterrows():
            record = row.to_dict()
    
            playback_order = index + 1
    
            record['PlaylistId'] = queue_id
            record['Playlist'] = queue_name
            record['TrackPlaybackOrder'] = playback_order
            record['CurrentPlaybackOrder'] = playback_order
            record['NowPlaying'] = 'N'
            record['CreateDate'] = datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S"
            )
            record['LastUpdateDate'] = datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S"
            )
    
            records.append(record)
    
        if len(records) > 0:
            now_playing_table.insert_multiple(records)
    
        self.CurrentPlaylistId = queue_id
    
        self.CurrentPlaylistInfo = pd.DataFrame([
            {
                'PlaylistId': queue_id,
                'Playlist': queue_name,
                'TrackCount': len(records)
            }
        ])
    
        return self.CurrentPlaylistInfo
 
    def setCurrentPlaylist(self,  PlaylistId):
#        sPlaylistId =  PlaylistId
#        sTrackId = TrackId
#        if sPlaylistId != self.CurrentPlaylistId:
#        self.clearNowPlayingTrack()
        self.clearCurrentPlaylist()
        self.addCurrentPlaylistToDB(PlaylistId)
        self.CurrentPlaylistInfo = self.getPlaylistInfoFromDB(PlaylistId)
        self.CurrentPlaylistId = PlaylistId
#            self.setNowPlayingTrack(sTrackId)  
#        elif sPlaylistId == self.CurrentPlaylistId and sTrackId != self.CurrentTrackId:
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
        
        
