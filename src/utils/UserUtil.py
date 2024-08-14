import bcrypt
import jwt
import os

class UserUtil():

    """ NOTE: Classe responsável por fazer tarefas relacionadas ao usuário """    

    @staticmethod
    def hash_password(password: str) -> str:       
        try: 
            salt = bcrypt.gensalt()        
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password
        except:
            return ''
        
    @staticmethod
    def check_password(hashed_password, user_password) -> bool:           
        try:
            return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
        except:
            return False
        
    @staticmethod
    def generate_token(data) -> str:
        try:
            return jwt.encode(data, os.getenv('SECRET_KEY'), algorithm="HS256")
        except:
            return ''
        

