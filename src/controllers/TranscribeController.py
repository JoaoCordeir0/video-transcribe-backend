import threading
import json
from pytube import YouTube
from src.controllers.ProgressController import ProgressController
from src.models.VideoLinkModel import VideoLinkModel
from src.models.VideoFileModel import VideoFileModel
from src.services.WhisperService import WhisperService
from src.services.TranslateService import TranslateService
from src.services.FileService import FileService
from src.services.MysqlService import MysqlService

class TranscribeController:

    """NOTE: Classe que controla as requisições de transcrições """
        
    params = None    

    def __init__(self, params: VideoLinkModel | VideoFileModel) -> None:
        self.params = params

    def exec_transcription(self, type) -> dict:             
        try:
            match type:
                case 'link':
                    threading.Thread(
                        target=self.start_video_link, 
                        args=(self.params, )
                    ).start()                    
                case 'file':                                        
                    FileService().save_file(self.params.file)

                    threading.Thread(
                        target=self.start_video_file, 
                        args=(self.params, )
                    ).start()

            return {
                'status': 'success',
                'message': f'Transcribe "{type}" started success',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
            }
    
    def start_video_file(self, params: VideoFileModel) -> None: 
        mysql = MysqlService()
        file_service = FileService()
        
        filename = params.file.filename
        
        # Salva o video no mysql
        video_id = mysql.save_transcribe((filename, ))         
        
        # Instância do controle de progresso 
        progress = ProgressController(
            user_id=params.user,
            video_id=video_id,
            mysql=mysql                
        )        
        job_id = progress.save(1)
                
        try:                       
            # Extraí para audio            
            audio_path, audio_name, video_name = file_service.get_audio_file(file_path=f'./tmp/{filename}')
            progress.update(30, job_id)
                
            # Chama o whisper para gerar os segmentos e texto           
            text_pt, segments = WhisperService().exec_transcribe(
                audio_path=audio_path,                 
            ) 
            progress.update(50, job_id)

            # Pega o texto em en
            text_en = TranslateService().translate_text_1(text=text_pt, language='en')
            progress.update(65, job_id)

            # Pega o texto em es
            text_es = TranslateService().translate_text_1(text=text_pt, language='es')
            progress.update(80, job_id)

            # Salva o texto e os segmentos no MYSQL                                                                       
            mysql.update_transcribe((video_name, text_pt, text_en, text_es, json.dumps(segments), video_id))
            progress.update(90, job_id)            
            
            # Exclui os arquivos usados da pasta tmp
            file_service.delete_files(files=[f'./tmp/{filename}', audio_path])            
            progress.update(100, job_id)            
        except Exception as e:
            progress.save_error(str(e), job_id)     
        
        # Fecha o  mysql
        mysql.close_conn()

    def start_video_link(self, params: VideoLinkModel) -> None:
        progress = ProgressController(params=params)        
        try:
            progress.save(1)         

            # Baixar o vídeo do YouTube  
            yt = YouTube(params.url)
            stream = yt.streams.filter().first()
            downloaded_file = stream.download(output_path="./tmp/videos")

            progress.save(100)            
        except Exception as e:
            progress.save_error(error=str(e))