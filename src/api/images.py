import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService
from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_file(UploadFile, background_tasks)
