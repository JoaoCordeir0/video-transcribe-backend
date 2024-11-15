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
    user = None

    def __init__(self, params: VideoLinkModel | VideoFileModel, user) -> None:
        self.params = params
        self.user = user

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

        # Nome do video        
        filename = params.file.filename
        
        # Plano do usuário
        plan = mysql.get_user_plan((self.user['id'], ))

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
            audio_path, _, video_name = file_service.get_audio_file(file_path=f'./tmp/{filename}')
            progress.update(30, job_id)
                
            # Chama o whisper para gerar os segmentos e texto           
            text, segments = WhisperService().exec_transcribe(
                audio_path=audio_path,                 
            ) 
            progress.update(50, job_id)
            
            # Salva em outros idiomas para os planos premium                        
            translate = TranslateService()
            if plan['title'] == 'Plano Premium':                                
                for lang in ['en', 'es']:                    
                    translate_text = translate.translate_text_1(text=text, language=lang)
                    translate_segments = translate.translate_segments_1(segments=segments, language=lang)
                            
                    mysql.save_transcribe_plus((video_id, lang, translate_text, json.dumps(translate_segments)))                

            if plan['title'] == 'Plano Premium Plus':                
                for lang in ['en', 'es', 'fr', 'de', 'it', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi']:                    
                    translate_text = translate.translate_text_2(text=text, language=lang)
                    translate_segments = translate.translate_segments_2(segments=segments, language=lang)
                            
                    mysql.save_transcribe_plus((video_id, lang, translate_text, json.dumps(translate_segments)))
            progress.update(70, job_id)                                

            # Salva o texto e os segmentos no MYSQL                                                                       
            mysql.update_transcribe((video_name, text, json.dumps(segments), video_id))
            progress.update(90, job_id)            
            
            # Exclui os arquivos usados da pasta tmp
            file_service.delete_files(files=[f'./tmp/{filename}', audio_path])            
            progress.update(100, job_id)            
        except Exception as e:
            progress.save_error(str(e), job_id)     
        
        # Fecha o  mysql
        mysql.close_conn()

    def start_video_link(self, params: VideoLinkModel) -> None:
        progress = ProgressController(params)        
        try:
            progress.save(1)         

            # Baixar o vídeo do YouTube  
            yt = YouTube(params.url)
            stream = yt.streams.filter().first()
            downloaded_file = stream.download(output_path="./tmp/videos")

            progress.save(100)            
        except Exception as e:
            progress.save_error(error=str(e))

    def generate_vtt(self): 
        ...