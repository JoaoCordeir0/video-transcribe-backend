from fastapi import APIRouter, Depends
from src.dto.UpdatePlanDTO import UpdatePlanDTO
from src.middleware.OAuth import OAuth
from src.controllers.UserController import UserController
from src.controllers.PlanController import PlanController
from src.controllers.TranscribeController import TranscribeController
from src.models.VideoLinkModel import VideoLinkModel
from src.models.VideoFileModel import VideoFileModel
from src.models.UserModel import LoginModel, RegisterModel

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


@router.get("/transcribe/{id}")
def transcribes(id: int, user: dict = Depends(OAuth().auth)):
    return UserController(None, user).get_transcribe(id)


@router.get("/transcribes")
def transcribes(user: dict = Depends(OAuth().auth)):
    return UserController(None, user).get_transcribes()


@router.get("/plans")
def transcribes():
    return PlanController().get_plans()


"""NOTE Rotas post da API -> """


@router.post("/user/login")
def login(params: LoginModel):
    return UserController(params, None).login()


@router.post("/user/register")
def register(params: RegisterModel):
    return UserController(params, None).register()


@router.post("/transcribe/video-file")
def exec_transcribe_file(
    params: VideoFileModel = Depends(VideoFileModel.get_form),
    user: dict = Depends(OAuth().auth),
):
    return TranscribeController(params, user).exec_transcription("file")


@router.post("/transcribe/video-link")
def exec_transcribe_link(params: VideoLinkModel):
    return TranscribeController(params).exec_transcription("link")


@router.post("/user/update-plan")
def update_plan(params: UpdatePlanDTO):
    return UserController(params, None).update_plan(params.user_id, params.plan_id)


@router.get("/user/update-plan/{user_id}")
def get_update_plan(user_id: int):
    return UserController(None, None).get_user_plan_data(user_id)
