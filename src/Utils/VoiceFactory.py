from src.DataClasses.Voice import Voice

class VoiceFactory:
    @staticmethod
    def create_voice(text: str, instrument: int, volume: int, tonality: str) -> Voice:
        return Voice(text, instrument, volume, tonality)
    
    @staticmethod
    def create_voices(quantity: int, instrument: int = 0, volume: int = 100, tonality: str = "C") -> list:
     
        voices = []
        for i in range(quantity):
            voice = VoiceFactory.create_voice(
                text=str(i + 1),
                instrument=instrument,
                volume=volume,
                tonality=tonality
            )
            voices.append(voice)
            
        return voices