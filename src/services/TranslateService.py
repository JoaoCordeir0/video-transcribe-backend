from googletrans import Translator

class TranslateService:

    """ NOTE: Classe responsável por fazer tradução """

    def __init__(self) -> None:
        pass
       
    def translate_text_1(self, text: str, language: str) -> str:
        try:
            translation = Translator().translate(text, dest=language)    
            return translation.text.replace('.', '. ')
        except Exception:
            return ''
        
    def translate_text_2(self, text: str, language: str) -> str:
        try:
            return 'In dev - deep-translator'
        except Exception:
            return ''