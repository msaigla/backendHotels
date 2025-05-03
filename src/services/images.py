import shutil

from fastapi import UploadFile, BackgroundTasks

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    def upload_file(self, file: UploadFile, background_tasks: BackgroundTasks):
        image_path = f"src/static/images/{file.filename}"
        with open(f"src/static/images/{file.filename}", "wb+") as f:
            shutil.copyfileobj(file.file, f)

        # resize_image.delay(image_path)
        background_tasks.add_task(resize_image, image_path)
