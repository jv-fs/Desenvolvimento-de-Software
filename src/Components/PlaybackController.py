class PlaybackController:

    def __init__(self, midi_player):
        self.midi_player = midi_player

    def play(self):
        self.midi_player.play()

    def stop(self):
        self.midi_player.stop()

    def restart(self):
        self.midi_player.restart()

    def toggle_loop(self):
        self.midi_player.toggle_loop()

    def is_playing(self):
        return self.midi_player.is_playing()

    def is_loop_enabled(self):
        return self.midi_player.is_loop_enabled()

    def set_volume(self, volume):
        self.midi_player.set_volume(volume)