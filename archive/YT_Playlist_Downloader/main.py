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
from tinydb import TinyDB, Query
#from pathlib import Path
import configparser
from datetime import datetime
#from difflib import SequenceMatcher

sHomeDirectory  = os.path.expanduser("~") + '/'
conf_file = sHomeDirectory +  '.piPod/piPod.conf'
config = configparser.ConfigParser()
config.sections()
config.read(conf_file)

sYouTubeMusicSource = 'YouTube Music'
#sHomeDirectory  = os.path.expanduser("~")

sWorkDirectory = sHomeDirectory + config['Default']['WorkDirectory']
sRelativeWorkDirectory = config['Default']['WorkDirectory']
sMusicRootDirectory = sHomeDirectory + config['Default']['MusicRootDirectory']
sCodec = 'mp3'
sPlaylistExtension = 'm3u'
sPlaylistRootDirectory = sHomeDirectory + config['Default']['PlaylistRootDirectory']
sURL = config['YT Downloader']['YT_URL']
sOauthFile = sHomeDirectory + config['Default']['OauthFileLocation'] + config['Default']['OauthFile']
sCookieFile = sHomeDirectory + config['YT Downloader']['CookiefileLocation'] + config['YT Downloader']['Cookiefile']
sPreferredQuality = config['YT Downloader']['preferredquality']
sTinyDBFileLocation = sHomeDirectory + config['TinyDB']['TinyDBLocation']
sTinyDBFile = sHomeDirectory + config['TinyDB']['TinyDBLocation']  + config['TinyDB']['TinyDBName'] 
sTrackNumber = ''

if os.path.isdir('/' + sWorkDirectory) == False:
    mode = 0o666
    os.mkdir('/' + sWorkDirectory,  mode)
    
def nvl(var, val):
  if var is None:
    return val
  return var
  
def nvl2(var, isNotNone, isNone):
  if var is None:
    return isNone
  return isNotNone
  
def getDB():
    if os.path.isfile(sTinyDBFile) == False:
        open(sTinyDBFile, 'a')

    db = TinyDB(sTinyDBFile)
    return db
#def initializeDB():
#    db = getDB()
#    if 'Album' not in db.tables():
#        tmp = db.table('Album')
#    else:
#         print("Table 'Album' exists")
         
def getTable(TableName):
    db = getDB()
    table = db.table(TableName)
    return table
    
def getYouTubeAutorization():
    yt = YTMusic("oauth.json")
    return yt
    
def addPlaylistToDB(Playlist,  Source):
    PlaylistQuery = Query()
    PlaylistTable = getTable('Playlist')
    sPlaylistId = Playlist ['playlistId']
    sPlaylist = Playlist ['title']
    sDescription = Playlist['description']
    if Source == None:
        sSource = sYouTubeMusicSource
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
#def deletePlaylist
#def deletePlaylistFromDB(deletePlaylist): 
    
def addAlbumToDB(AlbumId,  Album,  Source):
    AlbumQuery = Query()
    AlbumTable = getTable('Album')
#    print(Album)
    sAlbum = Album['title'] 
    sAlbumId = AlbumId
    sDescription = Album['description']
    sArtist = Album['artists'][0]['name']
    sArtistId = Album['artists'][0]['id']
    sYear = Album['year']
    sTrackCount = Album['trackCount']
    sDuration = Album['duration']
    if Source == None:
        sSource = sYouTubeMusicSource
    else:
        sSource = Source
        
    AlbumQueryResult = AlbumTable.search(AlbumQuery.Album.AlbumId == sAlbumId)
    if len(AlbumQueryResult) == 0 :
        AlbumTable.insert({'AlbumId ':  sAlbumId, 'Name' : sAlbum,  'Description' : sDescription, 'ArtistId' :  sArtistId, 'Artist' :  sArtist, 'Year' : sYear,  'TrackCount' :  sTrackCount, 'Duration' :  sDuration,  'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
    else:    
        AlbumTable.update({'Name' :  sAlbum,  'Description' : sDescription, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'Year' : sYear,  'TrackCount' :  sTrackCount, 'Duration' :  sDuration,  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  AlbumQuery.Album.AlbumId == sAlbumId )

def addArtistToDB(Playlist,  Album,  Track):
    artistQuery = Query()
    artistTable = getTable('Artist')
#    sPlaylistId = Playlist ['playlistId']
#    sPlaylist = Playlist ['title']
#    sTrackId = Track['videoId']
    sArtist = Track['artists'][0]['name']
    sArtistId = Track['artists'][0]['id']
    artistQueryResult = artistTable.search(artistQuery.artistTable.ArtistId == sArtistId)
    
    if len(artistQueryResult) == 0:
        artistTable.insert({'ArtistId' : sArtistId,  'ArtistName' :  sArtist, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
    else:
        artistTable.update({'ArtistId' : sArtistId,  'ArtistName' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  artistQuery.Artist.ArtistId == sArtistId)
    

def addTrackToDB(Playlist,  Album, Track, TrackPlaybackOrder,  FileLocation,  FileName,  Downloaded,  Source):
    trackQuery = Query()
    playlistTrackQuery = Query()
    trackTable = getTable('Track')
    playlistTrackTable = getTable('PlaylistTrack')
    
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
#    sYear = Album['year']
    sTrackNumber = getAlbumTrackNumber(Album, Track)
    sFileLocation = FileLocation
    sFileName = FileName
    if Source == None:
        sSource = sYouTubeMusicSource
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

def addSkippedTrackToDB(Playlist, SkippedTrack,  Source):
    skippedTrackQuery = Query()
    skippedTrackTable = getTable('SkippedTrack')
    
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
        sSource = sYouTubeMusicSource
    else:
        sSource = Source
    
    skippedTrackQueryResult = skippedTrackTable.search(skippedTrackQuery.SkippedTrack.TrackId == sSkippedTrackId)
    
    if len(skippedTrackQueryResult) == 0:
        skippedTrackTable.insert({'TrackId':  sSkippedTrackId, 'Title' : sTitle,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'PlaylistId' : sPlaylistId, 'Playlist' :  sPlaylist,   'Source' :  sSource, 'CreateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
    else:
        skippedTrackTable.update({'Title' :  sTitle,  'AlbumId' : sAlbumId, 'Album' : sAlbum, 'ArtistId' :  sArtistId,'Artist' :  sArtist, 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  skippedTrackQuery.SkippedTrack.TrackId == sSkippedTrackId)
     
    
def removePlaylistTracksFromDB(PlaylistId):
    db = getDB()
    sPlaylistId = PlaylistId
    playlistTrackTable = getTable('PlaylistTrack')
    playlistTrackQuery = Query()
    if 'PlaylistTrack' in db.tables():
        playlistTrackTable.remove(playlistTrackQuery.playlistTrackTable.PlaylistId == sPlaylistId)

def getPlaylistsFromDB():
    playlists =  getTable('Playlist')
    return  playlists
    
def getPlaylistsForDownload():
    playlistTable = getTable('Playlist')
    playlistQuery = Query()
    playlists = playlistTable.search(playlistQuery.playlstTable.FlagForDownload == 'Y' )
    return playlists

def getDowloadedPlaylists():
    playlistTable = getTable('Playlist')
    playlistQuery = Query()
    playlists = playlistTable.search(playlistQuery.playlstTable.FlagForDownload == 'Y' )
    return playlists
 
def getPlaylistTracksFromDB(currentPlaylistId):
    trackTable = getTable('Track')
    trackQuery = Query()
    queryResult = trackTable.search(trackQuery.Track.PlaylistId == currentPlaylistId)
    return queryResult
    
def  setPlaylistDownloaded(downloadedPlaylistId):
    playlistQuery = Query()
    playlistTable = getTable('Playlist')
    playlistTable.update({'Downloaded' : 'Y', 'FlagForDownload' : 'N', 'LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  playlistQuery.playlistTable.PlaylistId == downloadedPlaylistId)
    
def  setPlaylistForDownload(DownloadPlaylistId): 
    PlaylistTable = getTable('Playlist')
    PlaylistQuery = Query()
    PlaylistTable.update({'FlagForDownload' : 'Y','LastUpdateDate' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")},  PlaylistQuery.PlaylistId == DownloadPlaylistId) 
    
def getLibraryPlaylistsFromYouTube():
    yt = getYouTubeAutorization()
    userPlaylists = yt.get_library_playlists()
    return userPlaylists

def getPlaylistFromYouTube(downloadPlaylistId):
    yt = getYouTubeAutorization()
    userPlaylist = yt.get_playlist(downloadPlaylistId)
    return userPlaylist
    
def searchSubstituteTrackInYouTubeMusic(Track):
    sTrackName = Track['title']
    sArtist = Track['artists'][0]['name']
    sAlbum = Track['album']['name']
    sSearchString = sTrackName + ' ' + sArtist + ' ' + sAlbum
    sSearchFilter = 'songs'
    
    yt = getYouTubeAutorization()    
    searchResults = yt.search(sSearchString,  sSearchFilter)
#    print(searchResults)
    index = 0
    bestSong = {}
    albumSong = {}
    for song in searchResults:
        if index == 0: 
            firstSong = song
        index += 1
        if len(albumSong) == 0:
            album = getAlbumFromDB(song['album']['id'])
            if len(album) == 0:
                albumSong = song
    if len(albumSong) == 0:
        bestSong = albumSong
    else:
        bestSong = firstSong
#        sResultSearchString = song['title'] + ' ' + song['artists'][0]['name'] + ' ' + song['album']['name']
#        matchRatio = SequenceMatcher(None, sSearchString, sResultSearchString).ratio()
#        print(matchRatio, song['title'],  song['album']['name'], song['artists'][0]['name'] )
    return bestSong
    
    
def addYouTubeLibraryPlaylistsToDB(userPlaylists):
    for pl in userPlaylists:
        addPlaylistToDB(pl, sYouTubeMusicSource)
 
def downloadPlaylistTracksFromYouTube(downloadPlaylist):
    sPlaylistId = downloadPlaylist ['id']
    removePlaylistTracksFromDB(sPlaylistId)
#    playlistTrackTable = getTable('PlaylistTrack')
#    playlistTrackQuery = Query()
    
    iTrackPlaybackOrder = 0
    
    tracks= downloadPlaylist['tracks']
    for currentTrack in tracks:
        downloadTrack = currentTrack
        if downloadTrack['album']['id'][0:5] != 'MPREb':
            downloadTrack = searchSubstituteTrackInYouTubeMusic(currentTrack)
        if len(downloadTrack) > 0:
            currentAlbum = getTrackAlbum(downloadTrack)
            addAlbumToDB(downloadTrack['album']['id'],  currentAlbum,  sYouTubeMusicSource)
            addArtistToDB(downloadPlaylist,  currentAlbum,  downloadTrack)
            currentFileSystemTrackDirectory = getFileSystemDirectoryName(sMusicRootDirectory,  downloadTrack)
            currentFileSystemTrackName = getFileSystemTrackName(currentAlbum, downloadTrack, sCodec)
            downloadTrackFromYouTube(downloadPlaylist,  downloadTrack)
            iTrackPlaybackOrder += 1
            addTrackToDB(downloadPlaylist,  currentAlbum, downloadTrack, iTrackPlaybackOrder,  currentFileSystemTrackDirectory, currentFileSystemTrackName,  'Y',  sYouTubeMusicSource)

def downloadPlaylistFromYouTube(downloadPlaylistId):
    youTubePlaylist = getPlaylistFromYouTube(downloadPlaylistId)
#    print(youTubePlaylist)
    downloadPlaylistTracksFromYouTube(youTubePlaylist)
    setPlaylistDownloaded(downloadPlaylistId)

def getAlbumFromDB(albumId):
    albumTable = getTable('Album')
    albumQuery = Query()
    album = albumTable.search(albumQuery.albumTable.AlbumId == albumId )
    return album

def getAlbumName(track):
    if track['album'] is None:
        albumName = 'Unknown' # YouTubeSong['title']
    else:
        albumName = track['album']['name']
    return albumName
    
    
def getAlbumTrackNumber(album, track):
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

def getFileSystemDirectoryName(rootMusicDirectory, track):
    # Standard location is rootMusicDirectory/Artist/Album/
    # YouTube Video Location is rootMusicDirectory/YouTube/
#    isYouTubeVideo = False
    if track['artists'][0]['name'] is None:
        artist = 'Unknown'
    else:
        artist = track['artists'][0]['name']

    if track['album'] is None:
        # assume this is a user loaded video
#        isYouTubeVideo = True
        FileSystemDirectoryName = rootMusicDirectory + 'YouTube/'
    else:
        FileSystemDirectoryName = rootMusicDirectory + artist + '/'  + str(track['album']['name']) + '/'
    # sArtistDirectoryName = sMusicRootDirectory + str(workingSong['artist']) + '/'
    # sAlbumDirectoryName = sMusicRootDirectory + str(workingSong['artist']) + '/'  + str(workingSong['album']) + '/'
    return FileSystemDirectoryName

def getFileSystemTrackName(album, track,  codec):
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
        trackNumber = getAlbumTrackNumber(album, track)

    if isYouTubeVideo == False:
        fileSystemTrackName = artist + '_' + albumName + '_' + trackNumber + '_' + trackName
    else:
        fileSystemTrackName = artist + '_' + trackName + '_' + sVidID

    return fileSystemTrackName + '.' + codec

def downloadAudioFromYouTube(yt_url):
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
        'cookiefile' : sCookieFile, 
        'format': 'bestaudio/best',
        'outtmpl': sWorkDirectory + '%(title)s.%(ext)s',
#        'outtmpl':  'home/doug/.piPod/tmp/'+ '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': sCodec,
            'preferredquality': sPreferredQuality,
        }],
    }
    print(ydl_opts)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
#    os.chdir(sCurrentDirectory)

def getNewestMp3Filename(directory):
    # lists all mp3s in local directory
    print(directory)
    list_of_mp3s = glob.glob(directory + '*.mp3')
    # returns mp3 with highest timestamp value
    return max(list_of_mp3s, key = os.path.getctime)


def setId3Tags(album, track, downloadFile):
    try:
        currentTrack = music_tag.load_file(downloadFile)
    except OSError as error :
        print(error)
        print('Error opening file: ' + downloadFile)
    currentTrack['title'] = track['title']
    currentTrack['artist'] = track['artists'][0]['name']
    if track['album'] is None:
        currentTrack['album'] = 'Unknown' # YouTubeSong['title']
        currentTrack['comment'] = 'Most likey user uploaded video.  No Song or Album information available'
        i = 0
        for imgLoc in currentTrack['thumbnails']:
            tmp = urlopen(imgLoc['url'])
            data = bytearray(tmp.read())
            print(imgLoc)
            # print(data)
            # Image.
#            image = Image.open(io.BytesIO(data))
            # art.values(i).thumbnail([imageWidth, imageHeight]) == data
            if i == 0:
            # with open(image, 'rb') as img_in:
                currentTrack['artwork'] = io.BytesIO(data).getvalue()
                print(currentTrack['artwork'])
            else:
                currentTrack.append_tag('artwork', io.BytesIO(data).getvalue())
                print(currentTrack['artwork'])
            i += 1
    else:
        currentTrack['album'] = track['album']['name']
        yt = getYouTubeAutorization()
        album = yt.get_album(track['album']['id'])
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
        currentTrack['tracknumber'] = getAlbumTrackNumber(album, track)
#        art = currentSongTags['artwork']
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
    
def getTrackAlbum(track):
    if track['album'] is None:
         album = None
    else:
         yt = getYouTubeAutorization()
         album=yt.get_album(track['album']['id'])
#         print(album)
    return album

def downloadTrackFromYouTube(playlist,  track):
    album = getTrackAlbum(track)
    addAlbumToDB(track['album']['id'], album,  'YouTube Music')
    sYouTubeURL = sURL + track['videoId']
    downloadAudioFromYouTube(sYouTubeURL)
    sWorkingTrackFile = getNewestMp3Filename(sWorkDirectory)
    setId3Tags(album, track, sWorkingTrackFile)
    # iDurationSeconds = track['duration_seconds']
    sTrackDirectory = getFileSystemDirectoryName(sMusicRootDirectory, track)
    sTrackName = getFileSystemTrackName(album, track, sCodec)
    if not os.path.exists(sTrackDirectory):
        os.makedirs(sTrackDirectory)
    os.rename(sWorkingTrackFile, sTrackDirectory + sTrackName)
#    return
     
 
#  def downloadFlagedPlaylists:
     

# Press the green button in the gutter to run the script.

#    if pl['title'] == 'Golden Rain':
#        playlist = pl
#        break
        # print(playlist)
# print(getPlaylistsFromDB())
# exit()
#print(playlist['playlistId'])
# currentPlaylist = yt.get_playlist(playlist[])
#print(type(userPlayLists))
#for i in userPlayLists:
#    print(i)
# playList = yt.get_playlist('PLtoBJCi7zQr-vegQJ3z4q7Hz-5FqOMOPv')
#print(playList)
#ps = userPlayLists.pop(1)
#print(ps['playlistId'])
#playList = yt.get_playlist(ps['playlistId'])

# for playlist in userPlayLists:
#      print(playlist['title'], playlist['playlistId'])
# currentPlaylist = yt.get_playlist(playlist['playlistId'])
#print(currentPlaylist)
#currentPlaylistName = currentPlaylist['title']
# print(playlist)
#songs= currentPlaylist['tracks']
#iPodPlaylist = []
#for song in songs:
#     print(song)
#     if song['album'] is None:
#         songAlbum = None
#     else:
#         songAlbum = yt.get_album(song['album']['id'])

#     print(songAlbum)
#     str_YouTubeURL = sURL + song['videoId']
     # print(str_YouTubeURL)
#     download_audio(str_YouTubeURL)
     # print(newest_mp3_filename(sWorkDirectory))
#     sWorkingSongFile = newest_mp3_filename(sWorkDirectory)
#     workingSong = apply_id3_tags(songAlbum, song, sWorkingSongFile)
     # print(currentSongTags)

     #sSongName = str(workingSong['artist']) + '_' + str(workingSong['album']) + '_' + nvl(sTrackNumber, '00') + '_' + str(workingSong['title']) + '.mp3'
#     iDurationSeconds = song['duration_seconds']
#     sSongDirectory = getFileSystemDirectoryName(sMusicRootDirectory, song)
#     sSongName = getFileSystemSongName(songAlbum, song) + '.' + sCodec
#     if not os.path.exists(sSongDirectory):
#         os.makedirs(sSongDirectory)
#     os.rename(sWorkingSongFile, sSongDirectory + sSongName)
#     sIpodPlaylistEntry = '#EXTINF:' + str(iDurationSeconds) + ', ' + song['title'] + '\r\n' + os.path.abspath(sSongDirectory + sSongName)
#     iPodPlaylist.append(sIpodPlaylistEntry)
     # print(os.path.abspath(sSongDirectory + sSongName))

     # print(sSongDirectory + sSongName)

# iPlaylistLength = iPodPlayList.len()
#dUserPlaylists = getLibraryPlaylistsFromYouTube()
#addYouTubeLibraryPlaylistsToDB(dUserPlaylists)
#setPlaylistForDownload('PLtoBJCi7zQr-JjGJXiFXdnjsgC3FTwKKc')
downloadPlaylistFromYouTube('PLtoBJCi7zQr-JjGJXiFXdnjsgC3FTwKKc')
#initializeDB()
#track = {'videoId': 'auF8i4mm15o', 'title': 'New Dawn Fades', 'artists': [{'name': 'Joy Division', 'id': 'FEmusic_library_privately_owned_artist_detaila_po_CK3UjdWNusSeSxIMam95IGRpdmlzaW9u'}], 'album': {'name': 'Unknown Pleasures', 'id': 'FEmusic_library_privately_owned_release_detailb_po_CK3UjdWNusSeSxIRdW5rbm93biBwbGVhc3VyZXMiA2dwbQ'}, 'likeStatus': 'INDIFFERENT', 'inLibrary': None, 'thumbnails': [{'url': 'https://i9.ytimg.com/vi_locker/auF8i4mm15o/locker.png?sqp=-oaymwEGCDwQPCAA&rs=AMzJL3m5HXnOA4rESxcSd9-LCqpmXMbouw', 'width': 60, 'height': 60}, {'url': 'https://i9.ytimg.com/vi_locker/auF8i4mm15o/locker.png?sqp=-oaymwEGCHgQeCAA&rs=AMzJL3kg9pM7heU3U9JqveBh130AEm37SQ', 'width': 120, 'height': 120}], 'isAvailable': True, 'isExplicit': False, 'videoType': None, 'views': None, 'duration': '4:49', 'duration_seconds': 289, 'setVideoId': '289F4A46DF0A30D2'}
#print(searchSubstituteTrackInYouTubeMusic(track))

print('Done')

# {'playabilityStatus': {'status': 'OK', 'playableInEmbed': True, 'audioOnlyPlayability': {'audioOnlyPlayabilityRenderer': {'trackingParams': 'CAEQx2kiEwiNq47v0tiAAxVeyxYJHcXvB18=', 'audioOnlyAvailability': 'FEATURE_AVAILABILITY_ALLOWED'}}, 'miniplayer': {'miniplayerRenderer': {'playbackMode': 'PLAYBACK_MODE_ALLOW'}}, 'contextParams': 'Q0FFU0FnZ0I='}, 'streamingData': {'expiresInSeconds': '21540', 'formats': [{'itag': 18, 'mimeType': 'video/mp4; codecs="avc1.42001E, mp4a.40.2"', 'bitrate': 173158, 'width': 360, 'height': 360, 'lastModified': '1658153707362372', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '265241', 'audioSampleRate': '44100', 'audioChannels': 2, 'signatureCipher': 's=oQBE2ZkkvkWk08hhlfHIyvJouxqyS9IY9in-cHo_S-EICE-iS1UJ0zFYqarsAOC75eEu2mAtmgX7AMOF-2N0U2CcgIARw8JQ0qO55&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D18%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3DFSf5rsgF3FUpAhJgne0fuRAP%26cnr%3D14%26ratebypass%3Dyes%26dur%3D265.241%26lmt%3D1658153707362372%26mt%3D1691895440%26fvip%3D2%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1318224%26n%3DcEWxs1sivYljmiy0%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Ccnr%252Cratebypass%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRQIgYBo8AL8UEtX5IzGCeIlTvc6naXEB0aMzJRJlDc2uFcUCIQCA4kX6wKia1fGjyD3Hlzs33608vACw7syDPnavZz4xpg%253D%253D'}], 'adaptiveFormats': [{'itag': 137, 'mimeType': 'video/mp4; codecs="avc1.640020"', 'bitrate': 653445, 'width': 1080, 'height': 1080, 'initRange': {'start': '0', 'end': '738'}, 'indexRange': {'start': '739', 'end': '1394'}, 'lastModified': '1565805726931512', 'contentLength': '17437416', 'quality': 'hd1080', 'fps': 25, 'qualityLabel': '1080p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 526015, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DwmvzEHwTlE__RH3-4LHWFYbwYpqhi-RoZ3ydjO7r7a1CQICEyDR2FIOx2K-pXzb_YEop7YdyX2oMzJAHKQfXnnUh8bgIQRw8JQ0qOqq&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D137%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D17437416%26dur%3D265.200%26lmt%3D1565805726931512%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRAIgEBKvji2vj-dNFYw29Reh5694uXEZCfITe534BcVuRsACIDTT4pNT2LAHFuGulUHwVyYIlp5_t-RYyHi3oFBuWCBc'}, {'itag': 248, 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 616011, 'width': 1080, 'height': 1080, 'initRange': {'start': '0', 'end': '200'}, 'indexRange': {'start': '201', 'end': '1077'}, 'lastModified': '1565808719059595', 'contentLength': '17618917', 'quality': 'hd1080', 'fps': 25, 'qualityLabel': '1080p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 531490, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DwoSIG2votb7MHIid3D0zfE4_5lSY3oWxXaooqYPevp9BiAUAHcat5y6JRX3YvukUc-2eUCt0YaohXYAlbFzPae90OAhIQRw8JQ0qOdd&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D248%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D17618917%26dur%3D265.200%26lmt%3D1565808719059595%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAMfRJdrqzsWkO-Dage0Kdze8134Zan-qEEofQj168KHVAiEA-mOCOMT2F5ExKwC4Am1-WiutLQrEWpLtmNIOrnNxOJg%253D'}, {'itag': 136, 'mimeType': 'video/mp4; codecs="avc1.4d401f"', 'bitrate': 278139, 'width': 720, 'height': 720, 'initRange': {'start': '0', 'end': '735'}, 'indexRange': {'start': '736', 'end': '1391'}, 'lastModified': '1565806053478615', 'contentLength': '7453856', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 224852, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DghlK-FW51Qf0XbasxpsHFsQaLeetDpnPxUZG8hdAAtmBiAYW2QDZcBZwDwy39DTJ9PyO2WMBheYOMhAHj_Cs-tZtIAhIQRw8JQ0qOgg&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D136%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D7453856%26dur%3D265.200%26lmt%3D1565806053478615%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAJQeJYcNpH8NUVstfe9fRLJJx7ILQ0oV9omyiy54aGilAiEAiOTKONCt9ZXLItBMu2hlXP7zI_l0KGnMFk-xXiC9EYI%253D'}, {'itag': 247, 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 310082, 'width': 720, 'height': 720, 'initRange': {'start': '0', 'end': '200'}, 'indexRange': {'start': '201', 'end': '1075'}, 'lastModified': '1565808786171909', 'contentLength': '8712886', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 262832, 'approxDurationMs': '265200', 'signatureCipher': 's=%3DwlKmiFfG9C_i9BfMsPLLji6xOQRGlliqUs-mbsmMEtnAEiAA1qKIJ0Lilgng3tDWS4TUE4fndIwlT-4AL5mE9yM2bPAhIgRw8JQ0qOrr&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D247%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D8712886%26dur%3D265.200%26lmt%3D1565808786171909%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRAIgPPwSCW9iAzhD8RS4zjQV8Ymi6Q3ONwUaxvm2J6lauykCID5lguht2OgniPMsmecJdaHYv50N2PpvV9kQWeKYbyMX'}, {'itag': 135, 'mimeType': 'video/mp4; codecs="avc1.4d401e"', 'bitrate': 117429, 'width': 480, 'height': 480, 'initRange': {'start': '0', 'end': '735'}, 'indexRange': {'start': '736', 'end': '1391'}, 'lastModified': '1565805722141800', 'contentLength': '3172414', 'quality': 'large', 'fps': 25, 'qualityLabel': '480p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 95698, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DgFPYo_Js0vVHSaFlyiUSq06A3wc2Q7trv9hC__TWRMnAiAHtb1_8hRqWlwBre3ARM2xRGgxIxijUAMAsCczUop-PNAhIQRw8JQ0qO99&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D135%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D3172414%26dur%3D265.200%26lmt%3D1565805722141800%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAMxWMmRIHlOTz9AUJWSrY98_a24_xNSgtwiMhqap576XAiEA3Eowwdund9nRa6bQtrqK1GML4OFYZl5eX3o5qc2Am_k%253D'}, {'itag': 244, 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 140696, 'width': 480, 'height': 480, 'initRange': {'start': '0', 'end': '200'}, 'indexRange': {'start': '201', 'end': '1075'}, 'lastModified': '1565808786174726', 'contentLength': '3939527', 'quality': 'large', 'fps': 25, 'qualityLabel': '480p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 118839, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DAQQIdjKIuSx7Picfln2F91csLs97IiQ2adOn0ZZEDCQAiAyce_r_HQuQlxpi2_NRM4tkwtQQvbL2F_AfM96wmbJ5MAhIQRw8JQ0qONN&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D244%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D3939527%26dur%3D265.200%26lmt%3D1565808786174726%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRQIhAMV8Pyjc0UQzBWJS5tkYMx91QSvXQUWz4WjJFfoAIfQ7AiB_L5GdxrD496vzlqjB9EgjWkMpow1EXeNgeJD3P4MYEQ%253D%253D'}, {'itag': 134, 'mimeType': 'video/mp4; codecs="avc1.4d4015"', 'bitrate': 53709, 'width': 360, 'height': 360, 'initRange': {'start': '0', 'end': '736'}, 'indexRange': {'start': '737', 'end': '1392'}, 'lastModified': '1565805761610878', 'contentLength': '1467061', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 44255, 'highReplication': True, 'approxDurationMs': '265200', 'signatureCipher': 's=%3DEquDrL7wo6aJgYwnaGY3Np86IXjYklwnM63qbvbbT-iAEiAKRIg1odCBJoVlBglleK8yLsIVnQxatf3AaVOOiJriZPAhIgRw8JQ0qOJJ&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D134%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D1467061%26dur%3D265.200%26lmt%3D1565805761610878%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRAIgDRtWD53lu8FJIUDpDtF_pDX_Lg0yWuI_uk7nXg9I8lsCIDpqPLLHDH7P5FYb7Yasuf1LUpXMrGLy3ylFLpZWh58o'}, {'itag': 243, 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 75445, 'width': 360, 'height': 360, 'initRange': {'start': '0', 'end': '200'}, 'indexRange': {'start': '201', 'end': '1074'}, 'lastModified': '1565808786173079', 'contentLength': '2446195', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 73791, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D8bAXzJPs5PU9q0L4y0ulyTPSnztJwHvMTk6VHqIefUhAEiAwBTpWyukJHDkWDqyn6HoGXeK0E1KWnoaAHPs8mvG1vLAhIgRw8JQ0qO66&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D243%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D2446195%26dur%3D265.200%26lmt%3D1565808786173079%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRQIhAONlIy59fyNREoCKK6aQrHqwJdJJAOGgQHahp82JQEmYAiAy1A5JXMqVWajDmiLbVJpGIZ8kVAf2Q6gqV2jYVx2owg%253D%253D'}, {'itag': 133, 'mimeType': 'video/mp4; codecs="avc1.4d400c"', 'bitrate': 108382, 'width': 240, 'height': 240, 'initRange': {'start': '0', 'end': '734'}, 'indexRange': {'start': '735', 'end': '1390'}, 'lastModified': '1565805720918035', 'contentLength': '2921196', 'quality': 'small', 'fps': 25, 'qualityLabel': '240p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 88120, 'approxDurationMs': '265200', 'signatureCipher': 's=%3DgNkIc54edRPNgL8KEslCu79bn84nsam09BR1R0PAU2tAEiAQoocdg8_99IgIt5tOtBD3ivKdUbGPKESAFJGtspfjEMAhIgRw8JQ0qO55&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D133%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D2921196%26dur%3D265.200%26lmt%3D1565805720918035%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAJmLAjfup-h577CNbKQmFG66AX-mzR0g2QjWCX_r5hBVAiEAnJunr-WGT4I9M5cj7QmpH5TUm98IVglOl7XSgq_d-PE%253D'}, {'itag': 242, 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 45017, 'width': 240, 'height': 240, 'initRange': {'start': '0', 'end': '197'}, 'indexRange': {'start': '198', 'end': '1070'}, 'lastModified': '1565808786170670', 'contentLength': '1289109', 'quality': 'small', 'fps': 25, 'qualityLabel': '240p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 38887, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DAJAR7IgZOxx_MKQQfZ17iaEgdY9Ptt3x7NR1LDbqaVbDQICEYJTnUfPAquQhp3G0V9BknN1j7pZWUiA3qCopfkh0gKgIQRw8JQ0qOHH&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D242%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D1289109%26dur%3D265.200%26lmt%3D1565808786170670%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRAIgforZuwOg1--uP9GDm-z-V_WvYyVqFmfYyt-ZtSAXq2wCIHVw9MlaFfUa_57AhFWEuHJLtBqf5aoKRH2gBi8EmzaL'}, {'itag': 160, 'mimeType': 'video/mp4; codecs="avc1.4d400b"', 'bitrate': 43921, 'width': 144, 'height': 144, 'initRange': {'start': '0', 'end': '734'}, 'indexRange': {'start': '735', 'end': '1390'}, 'lastModified': '1565805710992341', 'contentLength': '1207774', 'quality': 'tiny', 'fps': 25, 'qualityLabel': '144p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 36433, 'approxDurationMs': '265200', 'signatureCipher': 's=%3DUHnc24ipTApdfRcutbPaGL0OBZM7WI1V1BwUXeskDs8AEiA3RI9ayiu4E-098lXdioOhhsH12gktQSYAzRK_uDU03KAhIgRw8JQ0qOFF&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D160%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D1207774%26dur%3D265.200%26lmt%3D1565805710992341%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRQIhAPceyFzcMYClV-Fe5bf-Eq2Rf-y-lRSHDTBal1oWx0h2AiAbDLwew9HdhviVE1fwtZTA3MhFG4Fmfj4BSpABr5BmKQ%253D%253D'}, {'itag': 278, 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 23147, 'width': 144, 'height': 144, 'initRange': {'start': '0', 'end': '197'}, 'indexRange': {'start': '198', 'end': '1067'}, 'lastModified': '1565808786171192', 'contentLength': '649569', 'quality': 'tiny', 'fps': 25, 'qualityLabel': '144p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 19594, 'approxDurationMs': '265200', 'signatureCipher': 's=%3D%3DA9caAYLjsRUn7YXzG8Gt9gibH163O1uyMAxGDUWHru4BiAFk30crILHX4PofRp0JptIAwzLk-EN9mbAFQd_oKuo_KAhIQRw8JQ0qOqq&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D278%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Dvideo%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D649569%26dur%3D265.200%26lmt%3D1565808786171192%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAPMlUbmKNj73wwtJH3wF2QHxiIparf5N-RjZkWAQVdQeAiEAx0Qp_TPXh3Wc5qYuPWVePGuFL-pO0V8jrEDixr-mHlc%253D'}, {'itag': 140, 'mimeType': 'audio/mp4; codecs="mp4a.40.2"', 'bitrate': 131018, 'initRange': {'start': '0', 'end': '667'}, 'indexRange': {'start': '668', 'end': '1023'}, 'lastModified': '1565805682853213', 'contentLength': '4294651', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 129552, 'highReplication': True, 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '265199', 'audioSampleRate': '44100', 'audioChannels': 2, 'loudnessDb': -4.2912645, 'signatureCipher': 's=%3DAuwtvaKMC1Wo33QWHYuqsWd11WRDWPYN5g9djqYOIejAEiApwC04NkntevLnaBrbZfjlddCGP1OWjpDA_0LjMQwVwMAhIgRw8JQ0qOMM&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D140%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Daudio%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D4294651%26dur%3D265.199%26lmt%3D1565805682853213%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRAIgCxbKmYGo9rEkwfotMjWv8HF3msgHn5_oZosEC6K7TE8CICsHXLrVVZxUa8FI9p7Ryo2HmgkX0QmAX4kKaQXfyY68'}, {'itag': 141, 'mimeType': 'audio/mp4; codecs="mp4a.40.2"', 'bitrate': 259254, 'initRange': {'start': '0', 'end': '667'}, 'indexRange': {'start': '668', 'end': '1023'}, 'lastModified': '1565805682386609', 'contentLength': '8538365', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 257568, 'audioQuality': 'AUDIO_QUALITY_HIGH', 'approxDurationMs': '265199', 'audioSampleRate': '44100', 'audioChannels': 2, 'loudnessDb': -4.2912645, 'signatureCipher': 's=GA3HekFvzMa28N3yVRV4nAn1y98u6yayk0JXG3HspBEICgUTLlbKbA7Wh2PzffbcAXkWQL5zJc1VAsLvB5Q9Dz0FgIARw8JQ0qONN&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D141%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Daudio%252Fmp4%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D8538365%26dur%3D265.199%26lmt%3D1565805682386609%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAISxf62jYAmpTYQEYGbSId_KcCMoEJgyLcGRsSoLt37KAiEAmIxwl415u9pDiCeF0p6-Va-0FWYkHUTBjgAxQdRi22M%253D'}, {'itag': 249, 'mimeType': 'audio/webm; codecs="opus"', 'bitrate': 48524, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '713'}, 'lastModified': '1565808682725632', 'contentLength': '1553555', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 46860, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '265221', 'audioSampleRate': '48000', 'audioChannels': 2, 'loudnessDb': -4.2912645, 'signatureCipher': 's=hmLv7TPOK3ssQDVIKWQCV4qlVEnRyuC9qhONg0KFcuFICY7bIi5qiYvGtnWZzp5tejJK4kyd678JA4Pd02DxYHGFgIARw8JQ0qOuu&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D249%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Daudio%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D1553555%26dur%3D265.221%26lmt%3D1565808682725632%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRQIhAM-sYTrDGEeoMnpVKTkhOEtbHrFJPZY_OeGEYeqQVlgQAiAdaJA6Oji_SGtqJVP8zwFlhYx5CefUF1JMYOo-45cIfQ%253D%253D'}, {'itag': 250, 'mimeType': 'audio/webm; codecs="opus"', 'bitrate': 64700, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '714'}, 'lastModified': '1565808683108993', 'contentLength': '2065578', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 62305, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '265221', 'audioSampleRate': '48000', 'audioChannels': 2, 'loudnessDb': -4.2912645, 'signatureCipher': 's=%3DoTh3s9EziMPyS-iuC0Ue-rtra12nX77vEhwTmlaicQvAEiAClSkdw2ZHbqFtoh4fh6ArUHGcXxVIY9bA0ajqUMAEZIAhIgRw8JQ0qOaa&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D250%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Daudio%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D2065578%26dur%3D265.221%26lmt%3D1565808683108993%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRgIhAICoxoi0mkKuvFBE-gSMvz0nZ0ZwnHU6Ko22ikWhw3vOAiEA-RRNwEQ3r18yY1_xrD6iRCqg7fi8hdPCVyhQXu0p8ZA%253D'}, {'itag': 251, 'mimeType': 'audio/webm; codecs="opus"', 'bitrate': 128791, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '714'}, 'lastModified': '1565808686221686', 'contentLength': '4151834', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 125233, 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '265221', 'audioSampleRate': '48000', 'audioChannels': 2, 'loudnessDb': -4.2912645, 'signatureCipher': 's=%3D%3Dwn48kisP9jaEaIaoyXVDIiHKcUCgZMItSG_qmW-99W9DQIC4y8-MVGMUARpvdczPdA-r8_O7jz0X75AgMXy5mCzGXcgIQRw8JQ0qO77&sp=sig&url=https://rr1---sn-jjpuxm5n-iv0s.googlevideo.com/videoplayback%3Fexpire%3D1691917362%26ei%3D0UfYZM3-Ot6W2_gPxd-f-AU%26ip%3D64.92.16.22%26id%3Do-AIMEQ-D1-eaKQS6m19Be6oKdE8rm591LBp_oAv3gznxz%26itag%3D251%26source%3Dyoutube%26requiressl%3Dyes%26mh%3D5A%26mm%3D31%252C29%26mn%3Dsn-jjpuxm5n-iv0s%252Csn-q4fzen7r%26ms%3Dau%252Crdu%26mv%3Dm%26mvi%3D1%26pl%3D19%26ctier%3DA%26pfa%3D5%26gcr%3Dus%26initcwndbps%3D1082500%26hightc%3Dyes%26siu%3D1%26spc%3DUWF9f-itjvHnd-AHxjcC-sDtN9YMJjQM8M6JoWYwcqXM%26vprv%3D1%26svpuc%3D1%26mime%3Daudio%252Fwebm%26ns%3Dh_Bkwxx9bVSEPGrH8SHmKg8P%26gir%3Dyes%26clen%3D4151834%26dur%3D265.221%26lmt%3D1565808686221686%26mt%3D1691895440%26fvip%3D2%26keepalive%3Dyes%26fexp%3D24007246%26c%3DWEB_REMIX%26txp%3D1311222%26n%3Dqbk7ZnPunWv4bKsZ%26sparams%3Dexpire%252Cei%252Cip%252Cid%252Citag%252Csource%252Crequiressl%252Cctier%252Cpfa%252Cgcr%252Chightc%252Csiu%252Cspc%252Cvprv%252Csvpuc%252Cmime%252Cns%252Cgir%252Cclen%252Cdur%252Clmt%26lsparams%3Dmh%252Cmm%252Cmn%252Cms%252Cmv%252Cmvi%252Cpl%252Cinitcwndbps%26lsig%3DAG3C_xAwRAIgeReI09_ysVLPTCX3KGCB2b5UrcS4YI1gymJNk3Q6qwsCID0pedcYYi7aMaRoiUaV5B1KLue188fi8sDkVg_NGcf7'}]}, 'playbackTracking': {'videostatsPlaybackUrl': {'baseUrl': 'https://s.youtube.com/api/stats/playback?cl=555117375&docid=v9SAJzSpG1s&ei=0UfYZM3-Ot6W2_gPxd-f-AU&fexp=23804281%2C23946420%2C23966208%2C23983296%2C23998056%2C24004644%2C24007246%2C24034168%2C24036947%2C24077241%2C24080738%2C24120819%2C24135310%2C24140247%2C24181174%2C24187377%2C24211178%2C24219713%2C24241378%2C24255543%2C24255545%2C24262346%2C24271463%2C24288664%2C24290971%2C24362095%2C24367580%2C24367821%2C24368306%2C24371778%2C24372101%2C24372110%2C24373396%2C24374315%2C24376978%2C24377910%2C24379043%2C24379061%2C24379125%2C24379354%2C24379527%2C24379544%2C24379962%2C24379969%2C24380264%2C24382551%2C24383022%2C24385612%2C24387154%2C24388708%2C24388718%2C24388735%2C24388746%2C24388759%2C24389132%2C24390675%2C24404640%2C24407191%2C24415864%2C24416290%2C24428788%2C24430726%2C24439361%2C24451319%2C24457384%2C24458317%2C24458324%2C24458329%2C24458839%2C24459435%2C24468724%2C24469243%2C24469818%2C24485421%2C24490421%2C24495060%2C24498300%2C24502747%2C24503257%2C24506625%2C24507808%2C24509570%2C24515366%2C24515423%2C24517093%2C24518452%2C24519102%2C24520147%2C24522523%2C24523472%2C24524098%2C24526642%2C24526774%2C24526783%2C24526794%2C24526801%2C24526808%2C24526815%2C24526823%2C24527295%2C24528356%2C24528463%2C24528468%2C24528475%2C24528482%2C24528552%2C24528557%2C24528573%2C24528582%2C24528642%2C24528651%2C24528661%2C24528666%2C24529352%2C24529367%2C24531246%2C24537200%2C24541967%2C24542452%2C24543276%2C24544156%2C24546075%2C24546216%2C24547937%2C24548627%2C24548628%2C24548882%2C24549087%2C24549485%2C24549704%2C24550285%2C24551130%2C24552156%2C24552606%2C24559326%2C24561140%2C24561150%2C24561208%2C24563746%2C24563969%2C24564452%2C24564582%2C24565904%2C24566538%2C24567652%2C24650809%2C24691334%2C24694842%2C24696321%2C24698452%2C24698880%2C24699598%2C39324156%2C39324185%2C39324221%2C39324314%2C39324324%2C39324331%2C39324341%2C39324379%2C39324479%2C39324496%2C39324563%2C45170058%2C51000316%2C51001633%2C51001918%2C51004017&ns=yt&plid=AAYCxS3kp-MmGJ3-&el=detailpage&len=266&of=Bx-Ym8pN175rNKraLrRltg&osid=AAAAAQZUvs0%3AAOeUNAYZowKdSpA5hwtptudGiUG7wBvASQ&uga=m57&vm=CAMQARgBOjJBQWpSVTZrdXcwd0xlYkNBV1hQcm1tb25lLURDNHV1ZVRPZFdBYThjYTVnUHh2ZTVpUWJQQVBta0tES19WekhOOXNtWHhJQXkwTFFXRzRFMmt2VlM0OUFBOV95RG9aQ0V6UE5JRVQyZ1Awdmh2N3lNSV8zY3ZKV1RNeHZQci15WlNuR3doAQ', 'headers': [{'headerType': 'USER_AUTH'}, {'headerType': 'VISITOR_ID'}, {'headerType': 'PLUS_PAGE_ID'}]}, 'videostatsDelayplayUrl': {'baseUrl': 'https://s.youtube.com/api/stats/delayplay?cl=555117375&docid=v9SAJzSpG1s&ei=0UfYZM3-Ot6W2_gPxd-f-AU&fexp=23804281%2C23946420%2C23966208%2C23983296%2C23998056%2C24004644%2C24007246%2C24034168%2C24036947%2C24077241%2C24080738%2C24120819%2C24135310%2C24140247%2C24181174%2C24187377%2C24211178%2C24219713%2C24241378%2C24255543%2C24255545%2C24262346%2C24271463%2C24288664%2C24290971%2C24362095%2C24367580%2C24367821%2C24368306%2C24371778%2C24372101%2C24372110%2C24373396%2C24374315%2C24376978%2C24377910%2C24379043%2C24379061%2C24379125%2C24379354%2C24379527%2C24379544%2C24379962%2C24379969%2C24380264%2C24382551%2C24383022%2C24385612%2C24387154%2C24388708%2C24388718%2C24388735%2C24388746%2C24388759%2C24389132%2C24390675%2C24404640%2C24407191%2C24415864%2C24416290%2C24428788%2C24430726%2C24439361%2C24451319%2C24457384%2C24458317%2C24458324%2C24458329%2C24458839%2C24459435%2C24468724%2C24469243%2C24469818%2C24485421%2C24490421%2C24495060%2C24498300%2C24502747%2C24503257%2C24506625%2C24507808%2C24509570%2C24515366%2C24515423%2C24517093%2C24518452%2C24519102%2C24520147%2C24522523%2C24523472%2C24524098%2C24526642%2C24526774%2C24526783%2C24526794%2C24526801%2C24526808%2C24526815%2C24526823%2C24527295%2C24528356%2C24528463%2C24528468%2C24528475%2C24528482%2C24528552%2C24528557%2C24528573%2C24528582%2C24528642%2C24528651%2C24528661%2C24528666%2C24529352%2C24529367%2C24531246%2C24537200%2C24541967%2C24542452%2C24543276%2C24544156%2C24546075%2C24546216%2C24547937%2C24548627%2C24548628%2C24548882%2C24549087%2C24549485%2C24549704%2C24550285%2C24551130%2C24552156%2C24552606%2C24559326%2C24561140%2C24561150%2C24561208%2C24563746%2C24563969%2C24564452%2C24564582%2C24565904%2C24566538%2C24567652%2C24650809%2C24691334%2C24694842%2C24696321%2C24698452%2C24698880%2C24699598%2C39324156%2C39324185%2C39324221%2C39324314%2C39324324%2C39324331%2C39324341%2C39324379%2C39324479%2C39324496%2C39324563%2C45170058%2C51000316%2C51001633%2C51001918%2C51004017&ns=yt&plid=AAYCxS3kp-MmGJ3-&el=detailpage&len=266&of=Bx-Ym8pN175rNKraLrRltg&osid=AAAAAQZUvs0%3AAOeUNAYZowKdSpA5hwtptudGiUG7wBvASQ&uga=m57&vm=CAMQARgBOjJBQWpSVTZrdXcwd0xlYkNBV1hQcm1tb25lLURDNHV1ZVRPZFdBYThjYTVnUHh2ZTVpUWJQQVBta0tES19WekhOOXNtWHhJQXkwTFFXRzRFMmt2VlM0OUFBOV95RG9aQ0V6UE5JRVQyZ1Awdmh2N3lNSV8zY3ZKV1RNeHZQci15WlNuR3doAQ', 'headers': [{'headerType': 'USER_AUTH'}, {'headerType': 'VISITOR_ID'}, {'headerType': 'PLUS_PAGE_ID'}]}, 'videostatsWatchtimeUrl': {'baseUrl': 'https://s.youtube.com/api/stats/watchtime?cl=555117375&docid=v9SAJzSpG1s&ei=0UfYZM3-Ot6W2_gPxd-f-AU&fexp=23804281%2C23946420%2C23966208%2C23983296%2C23998056%2C24004644%2C24007246%2C24034168%2C24036947%2C24077241%2C24080738%2C24120819%2C24135310%2C24140247%2C24181174%2C24187377%2C24211178%2C24219713%2C24241378%2C24255543%2C24255545%2C24262346%2C24271463%2C24288664%2C24290971%2C24362095%2C24367580%2C24367821%2C24368306%2C24371778%2C24372101%2C24372110%2C24373396%2C24374315%2C24376978%2C24377910%2C24379043%2C24379061%2C24379125%2C24379354%2C24379527%2C24379544%2C24379962%2C24379969%2C24380264%2C24382551%2C24383022%2C24385612%2C24387154%2C24388708%2C24388718%2C24388735%2C24388746%2C24388759%2C24389132%2C24390675%2C24404640%2C24407191%2C24415864%2C24416290%2C24428788%2C24430726%2C24439361%2C24451319%2C24457384%2C24458317%2C24458324%2C24458329%2C24458839%2C24459435%2C24468724%2C24469243%2C24469818%2C24485421%2C24490421%2C24495060%2C24498300%2C24502747%2C24503257%2C24506625%2C24507808%2C24509570%2C24515366%2C24515423%2C24517093%2C24518452%2C24519102%2C24520147%2C24522523%2C24523472%2C24524098%2C24526642%2C24526774%2C24526783%2C24526794%2C24526801%2C24526808%2C24526815%2C24526823%2C24527295%2C24528356%2C24528463%2C24528468%2C24528475%2C24528482%2C24528552%2C24528557%2C24528573%2C24528582%2C24528642%2C24528651%2C24528661%2C24528666%2C24529352%2C24529367%2C24531246%2C24537200%2C24541967%2C24542452%2C24543276%2C24544156%2C24546075%2C24546216%2C24547937%2C24548627%2C24548628%2C24548882%2C24549087%2C24549485%2C24549704%2C24550285%2C24551130%2C24552156%2C24552606%2C24559326%2C24561140%2C24561150%2C24561208%2C24563746%2C24563969%2C24564452%2C24564582%2C24565904%2C24566538%2C24567652%2C24650809%2C24691334%2C24694842%2C24696321%2C24698452%2C24698880%2C24699598%2C39324156%2C39324185%2C39324221%2C39324314%2C39324324%2C39324331%2C39324341%2C39324379%2C39324479%2C39324496%2C39324563%2C45170058%2C51000316%2C51001633%2C51001918%2C51004017&ns=yt&plid=AAYCxS3kp-MmGJ3-&el=detailpage&len=266&of=Bx-Ym8pN175rNKraLrRltg&osid=AAAAAQZUvs0%3AAOeUNAYZowKdSpA5hwtptudGiUG7wBvASQ&uga=m57&vm=CAMQARgBOjJBQWpSVTZrdXcwd0xlYkNBV1hQcm1tb25lLURDNHV1ZVRPZFdBYThjYTVnUHh2ZTVpUWJQQVBta0tES19WekhOOXNtWHhJQXkwTFFXRzRFMmt2VlM0OUFBOV95RG9aQ0V6UE5JRVQyZ1Awdmh2N3lNSV8zY3ZKV1RNeHZQci15WlNuR3doAQ', 'headers': [{'headerType': 'USER_AUTH'}, {'headerType': 'VISITOR_ID'}, {'headerType': 'PLUS_PAGE_ID'}]}, 'ptrackingUrl': {'baseUrl': 'https://www.youtube.com/ptracking?ei=0UfYZM3-Ot6W2_gPxd-f-AU&oid=Ta2MYghl4Z0lHK1qcf671g&plid=AAYCxS3kp-MmGJ3-&pltype=content&ptchn=843XEuTf3X4YO1Gpb9PuXA&ptk=youtube_single&video_id=v9SAJzSpG1s', 'headers': [{'headerType': 'USER_AUTH'}, {'headerType': 'VISITOR_ID'}, {'headerType': 'PLUS_PAGE_ID'}]}, 'qoeUrl': {'baseUrl': 'https://s.youtube.com/api/stats/qoe?cl=555117375&docid=v9SAJzSpG1s&ei=0UfYZM3-Ot6W2_gPxd-f-AU&event=streamingstats&fexp=23804281%2C23946420%2C23966208%2C23983296%2C23998056%2C24004644%2C24007246%2C24034168%2C24036947%2C24077241%2C24080738%2C24120819%2C24135310%2C24140247%2C24181174%2C24187377%2C24211178%2C24219713%2C24241378%2C24255543%2C24255545%2C24262346%2C24271463%2C24288664%2C24290971%2C24362095%2C24367580%2C24367821%2C24368306%2C24371778%2C24372101%2C24372110%2C24373396%2C24374315%2C24376978%2C24377910%2C24379043%2C24379061%2C24379125%2C24379354%2C24379527%2C24379544%2C24379962%2C24379969%2C24380264%2C24382551%2C24383022%2C24385612%2C24387154%2C24388708%2C24388718%2C24388735%2C24388746%2C24388759%2C24389132%2C24390675%2C24404640%2C24407191%2C24415864%2C24416290%2C24428788%2C24430726%2C24439361%2C24451319%2C24457384%2C24458317%2C24458324%2C24458329%2C24458839%2C24459435%2C24468724%2C24469243%2C24469818%2C24485421%2C24490421%2C24495060%2C24498300%2C24502747%2C24503257%2C24506625%2C24507808%2C24509570%2C24515366%2C24515423%2C24517093%2C24518452%2C24519102%2C24520147%2C24522523%2C24523472%2C24524098%2C24526642%2C24526774%2C24526783%2C24526794%2C24526801%2C24526808%2C24526815%2C24526823%2C24527295%2C24528356%2C24528463%2C24528468%2C24528475%2C24528482%2C24528552%2C24528557%2C24528573%2C24528582%2C24528642%2C24528651%2C24528661%2C24528666%2C24529352%2C24529367%2C24531246%2C24537200%2C24541967%2C24542452%2C24543276%2C24544156%2C24546075%2C24546216%2C24547937%2C24548627%2C24548628%2C24548882%2C24549087%2C24549485%2C24549704%2C24550285%2C24551130%2C24552156%2C24552606%2C24559326%2C24561140%2C24561150%2C24561208%2C24563746%2C24563969%2C24564452%2C24564582%2C24565904%2C24566538%2C24567652%2C24650809%2C24691334%2C24694842%2C24696321%2C24698452%2C24698880%2C24699598%2C39324156%2C39324185%2C39324221%2C39324314%2C39324324%2C39324331%2C39324341%2C39324379%2C39324479%2C39324496%2C39324563%2C45170058%2C51000316%2C51001633%2C51001918%2C51004017&ns=yt&osid=AAAAAQZUvs0%3AAOeUNAYZowKdSpA5hwtptudGiUG7wBvASQ&plid=AAYCxS3kp-MmGJ3-', 'headers': [{'headerType': 'USER_AUTH'}, {'headerType': 'VISITOR_ID'}, {'headerType': 'PLUS_PAGE_ID'}]}, 'atrUrl': {'baseUrl': 'https://s.youtube.com/api/stats/atr?docid=v9SAJzSpG1s&ei=0UfYZM3-Ot6W2_gPxd-f-AU&len=266&ns=yt&plid=AAYCxS3kp-MmGJ3-&ver=2', 'elapsedMediaTimeSeconds': 5, 'headers': [{'headerType': 'USER_AUTH'}, {'headerType': 'VISITOR_ID'}, {'headerType': 'PLUS_PAGE_ID'}]}, 'videostatsScheduledFlushWalltimeSeconds': [10, 20, 30], 'videostatsDefaultFlushIntervalSeconds': 40}, 'videoDetails': {'videoId': 'v9SAJzSpG1s', 'title': 'Surrender (Live)', 'lengthSeconds': '265', 'channelId': 'UC843XEuTf3X4YO1Gpb9PuXA', 'isOwnerViewing': False, 'isCrawlable': True, 'thumbnail': {'thumbnails': [{'url': 'https://lh3.googleusercontent.com/PmpHcsroU1K6Fgxq3c7d6VzdJhR4fMBhCFW04ApjMQXbyBSOKciK0yX8WGxTtS2i9SyG5606tv5Gri0N=w60-h60-l90-rj', 'width': 60, 'height': 60}, {'url': 'https://lh3.googleusercontent.com/PmpHcsroU1K6Fgxq3c7d6VzdJhR4fMBhCFW04ApjMQXbyBSOKciK0yX8WGxTtS2i9SyG5606tv5Gri0N=w120-h120-l90-rj', 'width': 120, 'height': 120}, {'url': 'https://lh3.googleusercontent.com/PmpHcsroU1K6Fgxq3c7d6VzdJhR4fMBhCFW04ApjMQXbyBSOKciK0yX8WGxTtS2i9SyG5606tv5Gri0N=w226-h226-l90-rj', 'width': 226, 'height': 226}, {'url': 'https://lh3.googleusercontent.com/PmpHcsroU1K6Fgxq3c7d6VzdJhR4fMBhCFW04ApjMQXbyBSOKciK0yX8WGxTtS2i9SyG5606tv5Gri0N=w544-h544-l90-rj', 'width': 544, 'height': 544}]}, 'allowRatings': True, 'viewCount': '254027', 'author': 'Cheap Trick', 'isPrivate': False, 'isUnpluggedCorpus': False, 'musicVideoType': 'MUSIC_VIDEO_TYPE_ATV', 'isLiveContent': False}, 'microformat': {'microformatDataRenderer': {'urlCanonical': 'https://music.youtube.com/watch?v=v9SAJzSpG1s', 'title': 'Surrender (Live at Nippon Budokan, Tokyo, JPN - April 1978) - YouTube Music', 'description': 'Provided to YouTube by Epic Surrender (Live at Nippon Budokan, Tokyo, JPN - April 1978) · Cheap Trick At Budokan ℗ 1979 Epic Records, a division of Sony M...', 'thumbnail': {'thumbnails': [{'url': 'https://i.ytimg.com/vi/v9SAJzSpG1s/maxresdefault.jpg', 'width': 1280, 'height': 720}]}, 'siteName': 'YouTube Music', 'appName': 'YouTube Music', 'androidPackage': 'com.google.android.apps.youtube.music', 'iosAppStoreId': '1017492454', 'iosAppArguments': 'https://music.youtube.com/watch?v=v9SAJzSpG1s', 'ogType': 'video.other', 'urlApplinksIos': 'vnd.youtube.music://music.youtube.com/watch?v=v9SAJzSpG1s&feature=applinks', 'urlApplinksAndroid': 'vnd.youtube.music://music.youtube.com/watch?v=v9SAJzSpG1s&feature=applinks', 'urlTwitterIos': 'vnd.youtube.music://music.youtube.com/watch?v=v9SAJzSpG1s&feature=twitter-deep-link', 'urlTwitterAndroid': 'vnd.youtube.music://music.youtube.com/watch?v=v9SAJzSpG1s&feature=twitter-deep-link', 'twitterCardType': 'player', 'twitterSiteHandle': '@YouTubeMusic', 'schemaDotOrgType': 'http://schema.org/VideoObject', 'noindex': False, 'unlisted': False, 'paid': False, 'familySafe': True, 'tags': ['Cheap Trick', 'CHEAP TRICK', 'チープトリック', '廉價把戲合唱團', 'At Budokan', 'Surrender'], 'availableCountries': ['AE', 'AR', 'AS', 'AT', 'AU', 'AW', 'BA', 'BD', 'BE', 'BG', 'BH', 'BM', 'BO', 'BR', 'BY', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GF', 'GP', 'GR', 'GT', 'GU', 'HK', 'HN', 'HR', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KE', 'KH', 'KR', 'KW', 'KY', 'LB', 'LI', 'LK', 'LT', 'LU', 'LV', 'MA', 'MK', 'MP', 'MQ', 'MT', 'MX', 'MY', 'NC', 'NG', 'NI', 'NL', 'NO', 'NP', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PR', 'PT', 'PY', 'QA', 'RO', 'RS', 'RU', 'SA', 'SE', 'SG', 'SI', 'SK', 'SV', 'TC', 'TH', 'TR', 'TW', 'UA', 'US', 'UY', 'VE', 'VI', 'VN', 'YT', 'ZA'], 'pageOwnerDetails': {'name': 'Cheap Trick - Topic', 'externalChannelId': 'UC843XEuTf3X4YO1Gpb9PuXA', 'youtubeProfileUrl': 'http://www.youtube.com/channel/UC843XEuTf3X4YO1Gpb9PuXA'}, 'videoDetails': {'externalVideoId': 'v9SAJzSpG1s', 'durationSeconds': '266', 'durationIso8601': 'PT4M26S'}, 'linkAlternates': [{'hrefUrl': 'android-app://com.google.android.youtube/http/youtube.com/watch?v=v9SAJzSpG1s'}, {'hrefUrl': 'ios-app://544007664/http/youtube.com/watch?v=v9SAJzSpG1s'}, {'hrefUrl': 'https://www.youtube.com/oembed?format=json&url=https%3A%2F%2Fmusic.youtube.com%2Fwatch%3Fv%3Dv9SAJzSpG1s', 'title': 'Surrender (Live at Nippon Budokan, Tokyo, JPN - April 1978)', 'alternateType': 'application/json+oembed'}, {'hrefUrl': 'https://www.youtube.com/oembed?format=xml&url=https%3A%2F%2Fmusic.youtube.com%2Fwatch%3Fv%3Dv9SAJzSpG1s', 'title': 'Surrender (Live at Nippon Budokan, Tokyo, JPN - April 1978)', 'alternateType': 'text/xml+oembed'}], 'viewCount': '254027', 'publishDate': '2015-07-31', 'category': 'Music', 'uploadDate': '2015-07-31'}}}
# dict_keys(['videoId', 'title', 'artists', 'album', 'likeStatus', 'thumbnails', 'isAvailable', 'isExplicit', 'videoType', 'duration', 'duration_seconds', 'setVideoId', 'feedbackTokens'])
# v9SAJzSpG1s Surrender (Live)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
