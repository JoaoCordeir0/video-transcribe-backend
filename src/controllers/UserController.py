from src.services.MysqlService import MysqlService
from src.utils.UserUtil import UserUtil

class UserController:

    """ NOTE: Classe que controla requisições da parte de usuário """
        
    params = None
    mysql = None

    def __init__(self, params) -> None:
        self.params = params
        self.mysql = MysqlService()
    
    def login(self) -> dict:                
        user = self.mysql.login_user((self.params.email, ))
        plan = self.mysql.get_user_plan((user['id'], ))
        token = UserUtil.generate_token({
            'id': user['id'],
            'name': user['name'], 
            'email': user['email'], 
            'plan_title': plan['title'], 
            'plan_validity': str(plan['validity'])
        })

        if UserUtil.check_password(user['password'].encode('utf-8'), self.params.password):
            return {
                'status': 'success',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'status': user['status'],
                    'plan': plan,                    
                },
                'access_token': token,                
            }    
        return {
            'status': 'error',
            'message': 'Incorrect email or password!'
        }