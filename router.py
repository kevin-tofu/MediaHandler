import os, sys
import io
from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
from fastapi import Response
from typing import List, Optional, Union

from PIL import Image
import MediaHandler
import cv2
import numpy as np


class myProcessor(MediaHandler.Processor):
    def __init__(self):
        super().__init__()

    async def main_files(self, \
                   process_name: str, \
                   fpath_files: List[str], \
                   fpath_dst: str, \
                   **kwargs
    ) -> dict:
        if process_name == "files":
            return dict(status = "OK")


    async def main_file(self, \
                  process_name: str, \
                  fpath_org: str, \
                  fpath_dst: str, \
                  **kwargs
    ) -> dict:
        
        if process_name == "image":
            img = Image.open(fpath_org).convert('L')
            img.save(fpath_dst)
            return dict(status = "OK")

        elif process_name == "video":
            return dict(status = "OK")
        
        elif process_name == "zip":
            return dict(status = "OK")
    
    async def main_BytesIO(self, process_name:str, fBytesIO: io.BytesIO, **kwargs):

        # img = cv2.imread(fBytesIO)
        img_pil = Image.open(fBytesIO)
        img_np = np.asarray(img_pil)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        ext = 'jpg'
        _, img_np = cv2.imencode(f'.{ext}', img_np)
        
        return Response(content = img_np.tostring(), \
                        media_type = f'image/{ext}'
        )

test_config = dict(
    PATH_DATA = "./temp"
)

handler = MediaHandler.Router(myProcessor(), MediaHandler.Config(**test_config))
test_router = APIRouter(prefix="")

@test_router.post('/image/')
async def image(file: UploadFile = File(...), \
                bgtask: BackgroundTasks = BackgroundTasks(),\
                test: Optional[int] = 0):
    
    params = dict(
        test = test
    )
    print(file.filename)
    return await handler.post_file("image", file, "jpg", bgtask, **params)


@test_router.post('/image-bytesio/')
async def image(file: UploadFile = File(...), \
                bgtask: BackgroundTasks = BackgroundTasks(),\
                test: Optional[int] = 0):
    
    params = dict(
        test = test
    )
    print(file.filename)
    return await handler.post_file_BytesIO("image-bytesio", file, "jpg", bgtask, **params)


@test_router.post('/video/')
async def video(file: UploadFile = File(...), \
                bgtask: BackgroundTasks = BackgroundTasks(),\
                test: Optional[int] = 0):
    """
    """

    params = dict(
        test = test
    )
    return await handler.post_file("video", file, "json", bgtask, **params)


@test_router.post('/zip/')
async def zip(file: UploadFile = File(...), \
            bgtask: BackgroundTasks = BackgroundTasks(),\
            test: Optional[int] = 0):
    """
    """
    params = dict(
        test = test
    )
    return await handler.post_file("zip", file, "json", bgtask, **params)


@test_router.post('/files/')
async def files(files: List[UploadFile], \
                bgtask: BackgroundTasks = BackgroundTasks(),\
                test: Optional[int] = 0):
    """
    """
    params = dict(
        test = test
    )
    # print(params)

    return await handler.post_files("files", files, "json", bgtask, **params)

