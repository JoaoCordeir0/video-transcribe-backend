from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import date
import os

class OAuth:

    """NOTE: Classe que controla a autenticação na API
    
       Utiliza-se Bearer Authentication
    """

    oauth = OAuth2PasswordBearer(tokenUrl='/')

    def __init__(self) -> None:
        pass

    # Valida o token e retorna o usuário
    def auth(self, token: str = Depends(oauth)):        
        return self.check_token(token)
    
    # Verifica se o token passado é igual ao setado, caso não gera uma exceção
    def check_token(self, token: str):
        secret_token = os.getenv('SERVICE_TOKEN') + str(date.today().day)
        if secret_token != token:    
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token',
                headers={ 'WWW-Authenticate': 'Bearer' },
            )