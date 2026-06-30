class TextController:

    def __init__(self, text_operator):
        self.text_operator = text_operator

    def load_data(self, path):
        self.text_operator.load_data(path)

    def get_text(self):
        return self.text_operator.getText()

    def set_text(self, text):
        self.text_operator.setText(text)

    def has_error(self):
        return self.text_operator.has_error()