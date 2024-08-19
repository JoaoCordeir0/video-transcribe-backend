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
    
    def login_user(self, params) -> dict:
        try:
            query = 'SELECT * FROM users WHERE email = %s'

            cursor = self.conn.cursor(dictionary=True)                    
            cursor.execute(query, params)            
            user = cursor.fetchall()
            cursor.close()
            return user[0]
        except Exception as e: 
            print(str(e))

    def get_user_transcribes(self, params) -> dict:
        try:
            print(params)
            data = []
            query1 = 'SELECT * FROM jobs INNER JOIN videos on videos.id = jobs.video WHERE jobs.user = %s'

            cursor1 = self.conn.cursor(dictionary=True)                    
            cursor1.execute(query1, params)            
            videos = cursor1.fetchall()

            data.append({
                'videos': videos
            })
            
            for i in videos:                
                query2 = 'SELECT * FROM videos_plus WHERE video = %s'

                cursor2 = self.conn.cursor(dictionary=True)                    
                cursor2.execute(query2, (i['video'], ))            
                videos_plus = cursor2.fetchall()
                
                data.append({
                    'videos_plus': videos_plus
                })

            cursor1.close()
            cursor2.close()            
            return data
        except Exception as e: 
            print(str(e))

    def save_user(self, params) -> int:
        try:
            query = 'INSERT INTO users (name, email, password, status) VALUES (%s, %s, %s, 1)'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            user = cursor.lastrowid
            self.conn.commit()                        
            cursor.close()            
            return user
        except Exception as e: 
            print(str(e))

    def get_user_plan(self, params) -> None:
        try:
            query = 'SELECT validity, title, description, price FROM user_plan INNER JOIN plans ON user_plan.plan = plans.id WHERE user = %s ORDER BY user_plan.id DESC LIMIT 1'

            cursor = self.conn.cursor(dictionary=True)                    
            cursor.execute(query, params)            
            plan = cursor.fetchall()
            cursor.close()
            return plan[0]
        except Exception as e: 
            print(str(e))

    def set_user_plan(self, params) -> None:
        try:
            query = 'INSERT INTO user_plan (user, plan, validity) VALUES (%s, %s, %s)'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            planID = cursor.lastrowid
            self.conn.commit()                        
            cursor.close()            
            return planID
        except Exception as e: 
            print(str(e))

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

    def save_transcribe_plus(self, params) -> None:
        try:
            query = 'INSERT INTO videos_plus (video, language, transcribe, segments) VALUES (%s, %s, %s, %s)'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            self.conn.commit()                        
            cursor.close()            
        except Exception as e: 
            print(str(e))

    def update_transcribe(self, params) -> None:
        try:
            query = 'UPDATE videos SET video_name = %s, transcribe = %s, segments = %s WHERE id = %s'

            cursor = self.conn.cursor()                    
            cursor.execute(query, params)
            self.conn.commit()                        
            cursor.close()            
        except Exception as e: 
            print(str(e))    

    def close_conn(self) -> None:
        self.conn.close()
