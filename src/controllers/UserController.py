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
        try:
            user = self.mysql.login_user((self.params.email, ))
            plan = self.mysql.get_user_plan((user['id'], ))
            token = UserUtil.generate_token({
                'id': user['id'],
                'name': user['name'], 
                'email': user['email'], 
                'plan_title': plan['title'], 
                'plan_validity': str(plan['validity'])
            })

            if not UserUtil.check_password(user['password'].encode('utf-8'), self.params.password):
                raise Exception("Incorrect email or password!")

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
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def register(self) -> dict:
        try:
            userID = self.mysql.save_user(
                (
                    self.params.name,
                    self.params.email,
                    UserUtil.hash_password(self.params.password),
                )
            )
            self.mysql.set_user_plan(
                (
                    userID,
                    self.params.plan,
                    self.params.validity,
                )
            )
            return {
                'status': 'success',
                'message': 'User register success!',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
            }
        