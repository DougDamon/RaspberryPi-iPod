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
            return

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
        self.connect()
        return self.client.status().get("state", "stop")

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
