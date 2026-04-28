from src.Utils.Importer import InputReader

class TextOperator:
    def __init__(self):
        self.text = None

    def load_data(self, local = None):
        if local: # In case a local path is provided, it means it is a board text, so we use the specific method to read from the board
            self.text = InputReader.LoadTextFromBoard(local)
        else:
            # If no local path is provided, it means we want to read from an archive, so we use the method to read from an archive
            path = "caminho/arquivo.txt"  # AQUI VAI TER A HOOK DA BIBLIOTECA QUE ABRE O EXPLORADOR DE ARQUIVOS, PARA O USUÁRIO SELECIONAR O ARQUIVO .TXT
            self.text = InputReader.LoadTextFromArchive(path)

    def generate_voices_text(self):

        for text in enumerate(self.text):
            yield text