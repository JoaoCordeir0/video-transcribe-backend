from pydantic import BaseModel

class UserModel(BaseModel):

    """ NOTE: Classe responsável por parametrizar o que deve ser passado na requisição de uma transcrição via link """
    
    email: str
    password: str