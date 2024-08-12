class ProgressController:

    """ NOTE: Classe que controla o progresso de execução da transcrição """
        
    video_id = None
    user_id = None
    mysql = None

    def __init__(self, user_id, video_id, mysql) -> None:
        self.user_id = user_id
        self.video_id = video_id
        self.mysql = mysql
    
    def save(self, progress) -> None:
        print(f'Progress: {progress}%')        

        return self.mysql.save_job_status(
            (
                self.user_id,
                self.video_id,
                progress,
                'in_progress' if progress < 100 else 'completed'
            )
        )

    def update(self, progress, job_id) -> None:
        print(f'Progress: {progress}%')        

        self.mysql.update_job_status(
            (               
                progress,
                'in_progress' if progress < 100 else 'completed',
                job_id
            )
        )
    
    def save_error(self, error, job_id) -> None:
        print(f'Erro: {error}%')  

        self.mysql.update_job_status(
            (               
                -1,
                error,
                job_id
            )
        )