from Hooks import TextOperator
from Utils import VoiceFactory
from Components import MIDIWriter


def main():
    text_operator = TextOperator()
    text_operator.load_data() # FALTA ESTA LÓGICA PARA DEFINIR SE VAI SER LOCAL OU DE ARQUIVO, DEPENDENDO DO FLUXO DE USUÁRIO
    
    midi_writer = MIDIWriter(mapping={})  # AQUI VAI O MAPEAMENTO REAL PARA CONVERSÃO DE TEXTO PARA MIDI (tem que pensar melhor aqui)
    voicesText = text_operator.generate_voices_text()

    for voiceData in voicesText:
        new_voice = VoiceFactory.create_voice(voiceData, instrument=1, volume=100, tonality="C")  # EXEMPLO DE PARÂMETROS
        midi_writer.voice_processor(new_voice)  # O MIDIWriter processa a voz criada