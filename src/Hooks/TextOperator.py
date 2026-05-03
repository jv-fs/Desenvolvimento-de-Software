from src.Utils.Importer import InputReader

class TextOperator:
    def __init__(self):
        self.text = None

    def load_data(self, source, is_path=False):
        if is_path:
            # If the source is a path, load from file
            self.voices_text = InputReader.LoadTextFromArchive(source)
        else:
            # Otherwise, load from board
            self.voices_text = InputReader.LoadTextFromBoard(source)
    
    def getText(self):
        return self.text