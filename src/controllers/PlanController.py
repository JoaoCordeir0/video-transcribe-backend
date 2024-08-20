from src.services.MysqlService import MysqlService
from src.utils.UserUtil import UserUtil

class PlanController:

    """ NOTE: Classe que controla requisições da parte de planos """
        
    mysql = None

    def __init__(self) -> None:       
        self.mysql = MysqlService()
    
    def get_plans(self) -> dict:
        try:            
            plans = self.mysql.get_plans()
            return {
                'status': 'success',
                'data': plans,
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
            }