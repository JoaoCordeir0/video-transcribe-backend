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
        
    def translate_segments_1(self, segments: dict, language: str) -> str:
        try:
            new_segments = []
            for segment in segments:                                          
                new_segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'content': self.translate_text_1(text=segment['content'], language=language)
                })
            return new_segments                
        except Exception:
            return ''
        
    def translate_segments_2(self, segments: dict, language: str) -> str:
        try:
            return 'In dev - deep-translator'
        except Exception:
            return ''