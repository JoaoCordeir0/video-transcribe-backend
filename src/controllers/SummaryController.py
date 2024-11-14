from src.models.SummaryModel import SummaryModel
import nlpcloud
import os

class SummaryController:

    """NOTE: Classe que controla as requisições de resumo """
        
    params = None    
    
    def __init__(self, params: SummaryModel) -> None:
        self.params = params

    def generate_summary(self) -> dict:             
        try:
            client = nlpcloud.Client('bart-large-cnn', os.getenv('TOKEN_AI_SUMMARY'))
            
            return client.summarization(self.params.text)
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
            }