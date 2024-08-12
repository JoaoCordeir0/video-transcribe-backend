import whisper

class WhisperService:

    """ NOTE: Classe responsável por usar o serviço de transcrição do whisper da OpenAI. Extraí segmentos de texto do audio """

    model = None        

    def __init__(self, model_name: str = 'base') -> None:        
        self.model = whisper.load_model(model_name)        

    def exec_transcribe(self, audio_path: str, task: str = 'transcribe') -> dict:                
        result = self.model.transcribe(
            audio=audio_path,         
            verbose=False, 
            fp16=False,
            task=task
        )        

        segments = []
        for segment in result['segments']:                        
            segments.append({
                'start': segment['start'], 
                'end': segment['end'], 
                'content': segment['text'].strip()
            })

        return [result['text'], segments]