import webvtt
from tqdm import tqdm
from src.services.TranslateService import TranslateService

class VTTService:

    """ NOTE: Classe responsável por gerar o arquivo .vtt que é usado para legenda """

    language = None

    def __init__(self, language: str) -> None:
        self.language = language

    def get_vtt_info(self, audio_name:str) -> str:
        file = audio_name.replace('.wav', f'-{self.language}.vtt')
        path = f'./tmp/AI-{file}'
        name = path.replace('./tmp/', '')
        return [path, name]
        
    def format_timestamp(self, s: str):
        hours = int(s // 3600)
        minutes = int((s % 3600) // 60)
        seconds = int(s % 60)
        milliseconds = int((s % 1) * 1000)
        return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'

    def generate_vtt(self, segments: dict, vtt_path: str) -> None:
        vtt = webvtt.WebVTT()
        for segment in tqdm(segments):
            text = segment['content']
            if self.language != 'pt' and self.language != 'en':
                text = TranslateService().translate_text_1(
                    text=text,
                    language=self.language
                )

            caption = webvtt.Caption(
                start=self.format_timestamp(s=segment['start']),
                end=self.format_timestamp(s=segment['end']),
                text=text
            )
            vtt.captions.append(caption)
        vtt.save(vtt_path)