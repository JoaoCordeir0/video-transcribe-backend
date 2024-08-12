import os
import mysql.connector

class MysqlService():

    """NOTE: Classe que executa consultas no banco de dados 
        
        Métodos e suas finalidades:

        save_job_status(): Salva o status da transcrição do video
        save_transcribe(): Salva a transcrição do video
        close_conn(): Fecha a conexão
    """
    
    conn = None

    def __init__(self) -> None:
        self.initialize_conn()

    def initialize_conn(self) -> None:
        self.conn = mysql.connector.connect(
            host=os.getenv('HOST_DATABASE'),
            user=os.getenv('USER_DATABASE'),
            password=os.getenv('PASSWORD_DATABASE'),
            database=os.getenv('NAME_DATABASE')
        )
    
    def save_job_status(self, params) -> int:
        try:
            query = 'INSERT INTO jobs (user, video, progress, status) VALUES (%s, %s, %s, %s)'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            job_id = cursor.lastrowid
            self.conn.commit()
            cursor.close()            
            return job_id
        except Exception as e: 
            print(str(e))

    def update_job_status(self, params) -> None:
        try:
            query = 'UPDATE jobs SET progress = %s, status = %s WHERE id = %s'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            self.conn.commit()
            cursor.close()            
        except Exception as e: 
            print(str(e))             

    def save_transcribe(self, params) -> int:
        try:
            query = 'INSERT INTO videos (video_name) VALUES (%s)'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            video_id = cursor.lastrowid
            self.conn.commit()                        
            cursor.close()            
            return video_id
        except Exception as e: 
            print(str(e))

    def update_transcribe(self, params) -> None:
        try:
            query = 'UPDATE videos SET video_name = %s, transcribe_pt = %s, transcribe_en = %s, transcribe_es = %s, segments = %s WHERE id = %s'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            self.conn.commit()                        
            cursor.close()            
        except Exception as e: 
            print(str(e))

    def close_conn(self) -> None:
        self.conn.close()
