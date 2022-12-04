import os, sys
from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
from typing import List, Optional, Union

from PIL import Image
import MediaHandler


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

