from src.Utils.Exporter import ExportMidiFile

class ExportController:

    def __init__(self, midi_player, text_operator):

        self.midi_player = midi_player
        self.text_operator = text_operator

    def save_midi(self, destination_path):

        ExportMidiFile.export(
            destination_path,
            self.midi_player.temp_midi_path
        )

    def save_text(self, destination_path):

        text = self.text_operator.getText()

        if isinstance(text, list):
            text = "\n".join(text)

        with open(
            destination_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                text if text is not None else ""
            )