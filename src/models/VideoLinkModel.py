from pydantic import BaseModel

class VideoLinkModel(BaseModel):

    """ NOTE: Classe responsável por parametrizar o que deve ser passado na requisição de uma transcrição via link """
    
    url: str
    user: int