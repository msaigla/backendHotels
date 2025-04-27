import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_file(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(f"src/static/images/{file.filename}", "wb+") as f:
        shutil.copyfileobj(file.file, f)

    resize_image.delay(image_path)
