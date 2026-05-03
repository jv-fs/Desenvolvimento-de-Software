from src.DataClasses.Voice import Voice

class VoiceFactory:
    @staticmethod
    def create_voice(text: str, instrument: int, volume: int, tonality: str) -> Voice:
        return Voice(text, instrument, volume, tonality)
    