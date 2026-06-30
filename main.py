from src.Components.TextController import TextController
from src.Components.CompilationController import CompilationController
from src.Components.InstrumentController import InstrumentController
from src.Components.PlaybackController import PlaybackController
from src.Components.ExportController import ExportController
from src.Components.MIDIPlayer import MIDIPlayer
from src.Hooks.TextOperator import TextOperator
from src.Components.MIDIWriter import MIDIWriter
from src.Interface.GUI import GUI
from src.Components.ActionsController import ActionsController

class main():
    
    @staticmethod
    def run():
        text_operator = TextOperator()
        midi_writer = MIDIWriter(mapping={}, text_operator=text_operator)  
        midi_player = MIDIPlayer()

        playback = PlaybackController(midi_player=midi_player)
        compilation = CompilationController(midi_writer=midi_writer, midi_player=midi_player)
        export = ExportController(midi_player=midi_player, text_operator=text_operator)
        instrument = InstrumentController(midi_writer=midi_writer)
        text = TextController(text_operator=text_operator)

        actions_controller = ActionsController(
            playback=playback,
            text=text,
            compilation=compilation,
            export=export,
            instrument=instrument
        )

        gui = GUI(actions_controller=actions_controller)
        gui.run()

if __name__ == "__main__":
    main().run()