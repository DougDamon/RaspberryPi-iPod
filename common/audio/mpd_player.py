from mpd import MPDClient, ConnectionError, CommandError


class MPDAudioPlayback:
    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.connected = False
        self.connect()

    def connect(self):
        if self.connected:
            try:
                self.client.ping()
                return
            except ConnectionError:
                self.connected = False
                try:
                    self.client.disconnect()
                except Exception:
                    pass
    
        self.client.connect("localhost", 6600)
        self.connected = True

    def disconnect(self):
        if not self.connected:
            return

        self.client.close()
        self.client.disconnect()
        self.connected = False

    def status(self):
        self.connect()
    
        try:
            return self.client.status()
        except ConnectionError:
            self.connected = False
            self.connect()
            return self.client.status()

    def current_song(self):
        self.connect()
        return self.client.currentsong()

    def play(self):
        self.connect()
        self.client.play()

    def pause(self):
        self.connect()
        self.client.pause(1)

    def resume(self):
        self.connect()
        self.client.pause(0)

    def stop(self):
        self.connect()
        self.client.stop()

    def next(self):
        self.connect()
        self.client.next()

    def previous(self):
        self.connect()
        self.client.previous()

    def seek_current(self, seconds):
        self.connect()
        self.client.seekcur(seconds)

    def volume_up(self, step=5):
        self.connect()
        self.client.volume(step)

    def volume_down(self, step=5):
        self.connect()
        self.client.volume(-step)

    def get_volume(self):
        self.connect()
        return int(self.client.status().get("volume", 0))

    def get_state(self):
        return self.status().get("state", "stop")

    def is_playing(self):
        return self.get_state() == "play"

    def get_elapsed(self):
        self.connect()
        status = self.client.status()
        return float(status.get("elapsed", 0))

    def get_duration(self):
        self.connect()
        status = self.client.status()
        return float(status.get("duration", 0))
    
    def clear_playlist(self):
        self.connect()
        self.client.clear()

    def add_track(self, path):
        self.connect()
        self.client.add(path)
    
    def add_tracks(self, paths):
        self.connect()
        self.client.clear()

        for path in paths:
            self.client.add(path)

    def play_position(self, position=0):
        self.connect()
        self.client.play(position)
    
    def get_current_song(self):
        return self.current_song()
    
    def get_current_file(self):
        song = self.current_song()
        return song.get("file")
    
    def repeat_off(self):
        self.connect()
        self.client.repeat(0)
        self.client.single(0)
    
    def repeat_playlist(self):
        self.connect()
        self.client.repeat(1)
        self.client.single(0)
    
    def repeat_one(self):
        self.connect()
        self.client.repeat(1)
        self.client.single(1)
    
    def shuffle_off(self):
        self.connect()
        self.client.random(0)
    
    def shuffle_on(self):
        self.connect()
        self.client.random(1)
        
    def get_playlist_position(self):
        status = self.status()
        song = status.get("song")
    
        if song is None:
            return None
    
        return int(song)
    
    def get_playlist_length(self):
        status = self.status()
        return int(status.get("playlistlength", 0))
