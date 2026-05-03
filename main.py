from src.Hooks.TextOperator import TextOperator
from src.Utils.VoiceFactory import VoiceFactory
from src.Components.MIDIWriter import MIDIWriter
from src.Components.GUI import GUI


def main():
    text_operator = TextOperator()
    midi_writer = MIDIWriter(mapping={})  # AQUI VAI O MAPEAMENTO REAL PARA CONVERSÃO DE TEXTO PARA MIDI (tem que pensar melhor aqui)
    
    voices = VoiceFactory.create_voices(quantity=5)

    callback_commander = { 
        "load_data": text_operator.load_data,
        "getText": text_operator.getText,
        "has_error": text_operator.has_error,
    }

    
    gui = GUI(callback_commander=callback_commander, voices=voices)
    gui.run()

if __name__ == "__main__":
    main()