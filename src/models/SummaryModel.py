from pydantic import BaseModel

class SummaryModel(BaseModel):

    """ NOTE: Classe responsável por parametrizar o que deve ser passado na requisição de um resumo """
    
    text: str