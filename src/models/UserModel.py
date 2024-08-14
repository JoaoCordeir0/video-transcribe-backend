from pydantic import BaseModel

class LoginModel(BaseModel):

    """ NOTE: Classe responsável por parametrizar o que deve ser passado na requisição de uma transcrição via link """
    
    email: str
    password: str

class RegisterModel(BaseModel):

    """ NOTE: Classe responsável por parametrizar o que deve ser passado na requisição de uma transcrição via link """
    
    name: str
    email: str
    password: str
    plan: int
    validity: str