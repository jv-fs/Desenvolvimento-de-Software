class InputReader():
    @staticmethod
    def LoadTextFromArchive( path ):
        """
            This function searches for a .txt file from the specified path and saves each line into an array.

            Args:
                path (str): it is the file location
            Returns:
                list: a list of strings, each one being a different voice
        """
        try:
            with open(path, 'r', encoding='utf-8') as archive:

                lines = archive.readlines()
                
                voicesText = [line.strip() for line in lines if line.strip()]
                
                return voicesText
        except FileNotFoundError:
            print("Erro: O arquivo não foi encontrado.")
            return []
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return []
