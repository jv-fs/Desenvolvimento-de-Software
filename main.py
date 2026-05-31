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
        actions_controller = ActionsController(midi_player=midi_player, text_operator=text_operator, midi_writer=midi_writer)

        gui = GUI(actions_controller=actions_controller)
        gui.run()

if __name__ == "__main__":
    main().run()