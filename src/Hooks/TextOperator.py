from src.Utils.Importer import InputReader

class TextOperator:
    def __init__(self):
        self.text = None
        self.error_message = None

    def load_data(self, source, is_path=True):
        self.error_message = None
        if is_path:
            # If the source is a path, load from file
            self.voices_text, self.error_message = InputReader.LoadTextFromArchive(source)
        else:
            # Otherwise, load from board
            self.voices_text, self.error_message = InputReader.LoadTextFromBoard(source)
    
    def getText(self):
        return self.text
    
    def has_error(self):
        return self.error_message is not None