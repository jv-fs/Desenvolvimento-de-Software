import shutil

class ExportMidiFile():
    
    @staticmethod
    def export(destination_path, temp_midi_path):
         
        if not temp_midi_path:
            raise RuntimeError("Nenhum MIDI compilado.")

        shutil.copy(temp_midi_path, destination_path)