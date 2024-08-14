from fastapi import APIRouter, Depends
from src.middleware.OAuth import OAuth
from src.controllers.UserController import UserController
from src.controllers.TranscribeController import TranscribeController
from src.models.VideoLinkModel import VideoLinkModel
from src.models.VideoFileModel import VideoFileModel
from src.models.UserModel import UserModel

router = APIRouter()

""" NOTE: Rotas get da API -> """
@router.get('/')
def main() -> object:
    return {
        'info': {
            'name': 'Video Transcribe',            
        },
        'dev': 'João Victor Cordeiro',        
    }

"""NOTE Rotas post da API -> """
@router.post('/user/login')
def login(params: UserModel) -> object:
    return UserController(params).login()

@router.post('/transcribe/video-file')
def exec_transcribe_file(params: VideoFileModel = Depends(VideoFileModel.get_form), user: dict = Depends(OAuth().auth)) -> object:
    return TranscribeController(params, user).exec_transcription('file')

@router.post('/transcribe/video-link')
def exec_transcribe_link(params: VideoLinkModel) -> object:
    return TranscribeController(params).exec_transcription('link')