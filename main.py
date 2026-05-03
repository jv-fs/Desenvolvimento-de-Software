from src.Hooks.TextOperator import TextOperator
from src.Utils.VoiceFactory import VoiceFactory
from src.Components.MIDIWriter import MIDIWriter
from src.Components.GUI import GUI


def main():
    text_operator = TextOperator()
    midi_writer = MIDIWriter(mapping={})  # AQUI VAI O MAPEAMENTO REAL PARA CONVERSÃO DE TEXTO PARA MIDI (tem que pensar melhor aqui)
    gui = GUI(on_load_callback=text_operator.load_data)
    gui.run()

if __name__ == "__main__":
    main()