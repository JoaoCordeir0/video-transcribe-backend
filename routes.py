from fastapi import APIRouter, Depends
from src.middleware.OAuth import OAuth
from src.controllers.TranscribeController import TranscribeController
from src.models.VideoLinkModel import VideoLinkModel
from src.models.VideoFileModel import VideoFileModel

router = APIRouter()

""" NOTE: Rotas get da API -> """
@router.get("/")
def main() -> object:
    return {
        "info": {
            "name": "Video Transcribe",            
        },
        "dev": "João Victor Cordeiro",        
    }

"""NOTE Rotas post da API -> """
@router.post("/transcribe/video-file")
def exec_transcribe(params: VideoFileModel = Depends(VideoFileModel.get_form)) -> object:
    return TranscribeController(params=params).exec_transcription('file')

@router.post("/transcribe/video-link")
def exec_transcribe(params: VideoLinkModel) -> object:
    return TranscribeController(params=params).exec_transcription('link')