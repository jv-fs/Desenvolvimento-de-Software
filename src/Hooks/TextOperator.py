from src.Utils.Importer import InputReader

class TextOperator:
    def __init__(self):
        self.text = None
        self.error_message = None

    def load_data(self, source, is_path=True):
        self.error_message = None
        if is_path:
            # If the source is a path, load from file
            self.text, self.error_message = InputReader.LoadTextFromArchive(source)
        else:
            # Otherwise, load from board
            self.text, self.error_message = InputReader.LoadTextFromBoard(source)
    
    def getText(self):
        return self.text
    
    def has_error(self):
        if self.error_message is not None:
            return self.error_message
        else:
            return None