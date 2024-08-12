from pydantic import BaseModel
from fastapi import File, UploadFile, Form

class VideoFileModel(BaseModel):

    """ NOTE: Classe responsável por parametrizar o que deve ser passado na requisição de uma transcrição via link """
    
    file: UploadFile = File(...)
    user: int

    @staticmethod
    def get_form(        
        file: UploadFile = File(...),        
        user: int = Form(None),
    ):
        return VideoFileModel(
            file=file,
            user=user
        )