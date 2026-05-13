class ActionsController:
    def __init__(self, midi_player):
        self.midi_player = midi_player

    def handle_play(self):
        self.midi_player.play()