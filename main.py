from src.Hooks.TextOperator import TextOperator
from src.Components.MIDIWriter import MIDIWriter
from src.Components.GUI import GUI


def main():
    text_operator = TextOperator()
    midi_writer = MIDIWriter(mapping={}, text_operator=text_operator)  # AQUI VAI O MAPEAMENTO REAL PARA CONVERSÃO DE TEXTO PARA MIDI (tem que pensar melhor aqui)

    #funcoes vindas de text_operator para o GUI
    callback_commander = { 
        "load_data": text_operator.load_data,
        "getText": text_operator.getText,
        "has_error": text_operator.has_error,
        "get_current_voice": midi_writer.get_voice_from_index,
        "create_voices": midi_writer.create_voices,
        "update_text": text_operator.setText
    }

    gui = GUI(callback_commander=callback_commander)
    gui.run()

if __name__ == "__main__":
    main()