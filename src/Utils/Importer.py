class InputReader():
    @staticmethod
    def LoadTextFromArchive( path ):
        """
            This function searches for a .txt file from the specified path and saves each line into an array.

            Args:
                path (str): it is the file location
            Returns:
                tuple: (list of strings, error_message) - error_message is None if successful
        """
        try:
            with open(path, 'r', encoding='utf-8') as archive:

                lines = archive.readlines()
                
                voicesText = [line.strip() for line in lines if line.strip()]
                
                return voicesText, None
        except FileNotFoundError:
            print("Erro: O arquivo não foi encontrado.")
            return [], "Arquivo não encontrado"
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return [], "Tipo de arquivo incorreto"



    @staticmethod
    def LoadTextFromBoard(text):
        """
        This function processes text from the GUI text area.

        Args:
            text (str): the text content
        Returns:
            tuple: (list of strings, error_message) - error_message is None if successful
        """
        try:
            if not text or not text.strip():
                return [], "Texto vazio"
            
            lines = text.split('\n')
            voicesText = [line.strip() for line in lines if line.strip()]
            
            return voicesText, None
        except Exception as e:
            print(f"Erro ao processar texto: {e}")
            return [], "Erro ao processar texto"
