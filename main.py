from src.Components.MIDIPlayer import MIDIPlayer
from src.Hooks.TextOperator import TextOperator
from src.Components.MIDIWriter import MIDIWriter
from src.Interface.GUI import GUI
from src.Components.ActionsController import ActionsController


def main():
    text_operator = TextOperator()
    midi_writer = MIDIWriter(mapping={}, text_operator=text_operator)  
    midi_player = MIDIPlayer()

    #Usa Alta ordem para passar as funções necessárias para o funcionamento do GUI
    callback_commander = { 
        "load_data": text_operator.load_data,
        "getText": text_operator.getText,
        "has_error": text_operator.has_error,
        "get_current_voice": midi_writer.get_voice_from_index,
        "create_voices": midi_writer.create_voices,
        "update_text": text_operator.setText,
        "compile_tracks": midi_writer.append_tracks_to_midi_file,
        "create_temp_midi_file": midi_writer.create_temp_midi_file,
        "cleanup": midi_writer.cleanup,
        "set_temp_midi_path": midi_player.set_midi_temp,
        "play": midi_player.play
    }

    actions_controller = ActionsController(midi_player)
    gui = GUI(callback_commander=callback_commander, actions_controller=actions_controller)
    gui.run()

if __name__ == "__main__":
    main()