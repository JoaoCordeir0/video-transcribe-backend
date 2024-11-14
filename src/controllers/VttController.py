from src.services.VTTService import VTTService
from src.services.MysqlService import MysqlService
import json
import random 

class VttController:

    """NOTE: Classe que controla as requisições de vtt """

    def __init__(self) -> None:
        ...

    def generate_vtt(self, id): 
        mysql = MysqlService()
        vtt = VTTService('pt')

        segments = json.loads(mysql.get_vtt((id, ))['segments'])

        file = f'tmp/legenda_pt_{random.randint(4351, 189263)}.vtt'
        vtt = vtt.generate_vtt(segments, file)
        
        return {
            'file': file
        }
    
    def generate_vtt_plus(self, id): 
        return {
            'oi': 'oi'
        }