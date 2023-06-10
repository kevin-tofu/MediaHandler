import os, sys

import io
from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
from fastapi import Response
from typing import List, Optional, Union

from PIL import Image

# print(f"{os.pardir}/mediarouter")
# sys.path.append(f"{os.pardir}/mediarouter/")
# print(sys.path)

import mediarouter
import cv2
import numpy as np


class myProcessor(mediarouter.processor):
    def __init__(self):
        super().__init__()

    async def post_files_process(
        self,
        process_name: str,
        fpath_files: List[str],
        fpath_dst: Optional[str] = None,
        **kwargs
    ) -> dict:
        if process_name == "files":
            return dict(status = "OK")


    async def post_file_process(
        self,
        process_name: str,
        fpath_org: str,
        fpath_dst: Optional[str] = None,
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
    
    async def post_BytesIO_process(
        self,
        process_name :str,
        fBytesIO: io.BytesIO,
        fname_org: str,
        extension: str = 'jpg',
        **kwargs
    ):

        img_pil = Image.open(fBytesIO)
        img_np = np.asarray(img_pil)
        # print(img_np.shape) # (h, w, 3)
        
        # do stuff

        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        _, img_np = cv2.imencode(f'.{extension}', img_np)
        # print(img_np.shape) # (h*w*3)
        return Response(
            content = img_np.tostring(),
            media_type = f'image/{extension}'
        )


test_config = dict(
    PATH_DATA = "./temp"
)

handler = mediarouter.router(myProcessor(), mediarouter.config(**test_config))
test_router = APIRouter(prefix="")

@test_router.post('/image')
async def image(
    file: UploadFile = File(...),
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    
    params = dict(
        test = test
    )
    print(file.filename)
    return await handler.post_file("image", file, "jpg", bgtask, **params)


@test_router.post('/image-bytesio')
async def image(
    file: UploadFile = File(...),
    extension: str = 'jpg',
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    
    params = dict(
        extension=extension,
        test = test
    )
    print(file.filename)
    return await handler.post_file_BytesIO("image-bytesio",
                                           file,
                                           bgtask,
                                           **params)


@test_router.post('/video')
async def video(
    file: UploadFile = File(...),
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    """
    """

    params = dict(
        test = test
    )
    return await handler.post_file("video", file, "json", bgtask, **params)


@test_router.post('/zip')
async def zip(
    file: UploadFile = File(...),
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    """
    """
    params = dict(
        test = test
    )
    return await handler.post_file("zip", file, None, bgtask, **params)


@test_router.post('/files')
async def files(
    files: List[UploadFile],
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    """
    """
    params = dict(
        test = test
    )
    # print(params)

    return await handler.post_files("files", files, "json", bgtask, **params)

