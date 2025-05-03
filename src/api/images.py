from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_file(file, background_tasks)
