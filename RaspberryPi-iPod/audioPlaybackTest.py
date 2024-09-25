import os
import music_tag
import pygame
from pygame import mixer
from datetime import datetime
import time
from common.pipodconfiguration import piPodConfiguration
from common.musicdatabase import MusicDB

from mutagen.mp3 import MP3

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

musicDB = MusicDB()
config = piPodConfiguration()
MusicRootDirectory = config.MusicRootDirectory

done = False

playlists = musicDB.getDownloadedPlaylists()
for playlist in playlists:
#    print(type(playlist))
    print(playlist['Playlist'] +'       ' + playlist['PlaylistId']  )


playlistTracks = musicDB.getPlaylistTracksFromDB('PLtoBJCi7zQr9FBKCK-QXMcOlQj5IwHvPF')


for currentPlaylistTrack in playlistTracks:
    currentTrack = musicDB.getTrackFromDB(currentPlaylistTrack['TrackId'])
#    print(type(currentTrack))
    print(currentTrack['Title'],  currentTrack['FileLocation'],  currentTrack['FileName'])
    trackFileLocation = os.path.join(currentTrack['FileLocation'], currentTrack['FileName'])
    audio = MP3(trackFileLocation)
    trackLength = audio.info.length
    minutes, seconds = divmod(trackLength, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours,  minutes,  seconds)
    break
    print(trackFileLocation)
    pygame.mixer.music.load(trackFileLocation)
    print('start play/')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        print("Playing...")
        print(audio.info.length)
        clock.tick(1000)
    
#    pygame.event.wait()
#    time.sleep(10)
    print('end play')
#    while not done:
#        pygame.mixer.music.load(trackFileLocation)
        
        


    
    
    
