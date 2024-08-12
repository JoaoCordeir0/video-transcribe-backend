import os
from moviepy.editor import VideoFileClip

class FileService():

    """ NOTE: Classe responsável por formatar o caminho do audio e realizar extração de audio caso necessário """

    def __init__(self) -> None:
        pass

    def save_file(self, file):
        if not file or file.filename == '':
            return None
        
        path = os.path.join('tmp', file.filename)
        
        with open(path, 'wb') as f:
            f.write(file.file.read())   

        return file
    
    def delete_files(self, files: list) -> None:
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def get_audio_file(self, file_path: str) -> list:
        if '.wav' in file_path:
            audio_name = file_path.replace('./tmp/', '')
            video_name = audio_name.replace('.wav', '.mp4')
            return [file_path, audio_name, video_name]
        else: 
            audio_path = file_path.replace('.mp4', '.wav')
            audio_name = audio_path.replace('./tmp/', '')
            video_name = audio_name.replace('.wav', '.mp4')
            
            self.extract_audio(video_path=file_path, audio_path=audio_path)
            
            return [audio_path, audio_name, video_name]

    def extract_audio(self, video_path: str, audio_path: str) -> None:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)        
        os.remove(video_path)