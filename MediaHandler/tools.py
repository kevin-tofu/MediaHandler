
import os
import time
from typing import Optional, Union, List, Tuple

from fastapi import UploadFile
from fastapi import HTTPException

import uuid
import shutil
import enum

from MediaHandler.logconf import medialogger
logger = medialogger(__name__)
print('__name__', __name__)

import numpy as np
from PIL import Image
from io import BytesIO

class FileType(enum.Enum):
    JSON = 1
    IMAGE = 2
    VIDEO = 3
    ZIP = 4
    SOMETHINGELSE = 2000
    
extensions_image_base = ('jpg', 'jpeg', 'png', 'tiff')
extensions_video_base = ('mp4', 'avi', 'mov', 'wmv', 'webm')


def get_file_extension(fname: str):
    # fname_without_ext = os.path.splitext(fname)[0]
    extension = os.path.splitext(fname)[-1][1::]
    return extension

def get_mediatype(fpath: str):
    ext = get_file_extension(fpath)
    if ext in extensions_image:
        return f"image/{ext}"
    elif ext in extensions_video:
        return f"video/{ext}"
    elif ext in extensions_json:
        return f"application/{ext}"
    elif ext in extensions_zip:
        return f"application/{ext}"
    else:
        return FileType.SOMETHINGELSE


def check_filetype(fpath: str, \
                   extensions_image: Tuple[str] = extensions_image_base,\
                   extensions_video: Tuple[str] = extensions_video_base, \
                   extensions_json: Tuple[str] = ("json"), \
                   extensions_zip: Tuple[str] = ("zip")):
    
    ext = get_file_extension(fpath)
    if ext in extensions_image:
        return FileType.IMAGE
    elif ext in extensions_video:
        return FileType.VIDEO
    elif ext in extensions_json:
        return FileType.JSON
    elif ext in extensions_zip:
        return FileType.ZIP
    else:
        return FileType.SOMETHINGELSE

def error_handling_ext(ext_i: str, allowed_extensions: Tuple[str]):
    # extention_zip = ext_i.lower() in allowed_extensions
    if not ext_i.lower() in allowed_extensions:
        raise HTTPException(status_code=400, detail="The file is NOT {}".format(allowed_extensions))

def error_handling_zip_fpath(fpath: str, allowed_extensions: Tuple[str] = ('zip')):
    error_handling_ext(get_file_extension(fpath), allowed_extensions)

def error_handling_image_fpath(fpath: str, allowed_extensions: Tuple[str] = ('jpg', 'jpeg', 'png', 'tiff')):
    error_handling_ext(get_file_extension(fpath), allowed_extensions)

def error_handling_image_json(fpath: str, allowed_extensions: Tuple[str] = ('json')):
    error_handling_ext(get_file_extension(fpath), allowed_extensions)

def error_handling_zip(file: UploadFile, allowed_extensions: Tuple[str] = ('zip')):
    error_handling_ext(file.filename.split('.')[-1], allowed_extensions)

def error_handling_image(file: UploadFile, allowed_extensions: Tuple[str] = ('jpg', 'jpeg', 'png', 'tiff')):
    error_handling_ext(file.filename.split('.')[-1], allowed_extensions)

def error_handling_video(file: UploadFile, allowed_extensions: Tuple[str] = ('mp4', 'avi', 'mov', 'wmv', 'webm')):
    error_handling_ext(file.filename.split('.')[-1], allowed_extensions)

def error_handling_json(file: UploadFile, allowed_extensions: Tuple[str] = ('json')):
    error_handling_ext(file.filename.split('.')[-1], allowed_extensions)

def fname2uuid(fname: str):

    myuuid = str(uuid.uuid4())
    fname_ext = get_file_extension(fname)
    fname_uuid = f"{myuuid}.{fname_ext}"

    return fname_uuid, myuuid

def make_fname_uuid(ext: str):

    myuuid = str(uuid.uuid4())
    fname_uuid = f"{myuuid}.{ext}"

    return fname_uuid, make_fname_uuid

def addstr2fname(fname: str, addstr: str, ext = Optional[str]):

    if ext is None:
        fname_ext = os.path.splitext(fname)[-1]
    elif type(ext) is str:
        fname_ext = f".{ext}"
    else:
        fname_ext = ""

    fname_base = os.path.splitext(os.path.basename(fname))[0]
    fname_ret = f"{fname_base}{addstr}{fname_ext}"

    return fname_ret



def remove_dir(path_dir: str, sleep_sec: int=5) -> None:
    time.sleep(sleep_sec)
    if os.path.exists(path_dir) == True:
        shutil.rmtree(path_dir)
        logger.info(f'removed : {path_dir}')

def remove_file(path_file: str, sleep_sec: int=5) -> None:

    # logger.info('timer')
    time.sleep(sleep_sec)
    if os.path.exists(path_file) == True:
        os.unlink(path_file)
        logger.info(f'removed : {path_file}')

def remove_files(path_files: str, sleep_sec: int=5) -> None:

    # logger.info('timer')
    time.sleep(sleep_sec)
    for path_file in path_files:
        if os.path.exists(path_file) == True:
            os.unlink(path_file)
            logger.info(f'removed : {path_file}')


async def read_image(file) -> Image.Image:

    logger.debug("read_imagefile")
    image = Image.open(BytesIO(await file.read()))
    return np.asarray(image)

async def save_image(_path: str, \
                     _fname: str, \
                     file: UploadFile, 
                     test: Optional[Union[None, int]]=None):
    try:
        logger.info("save_image")
        image = Image.open(BytesIO(await file.read()))
        image.save(f"{_path}/{_fname}")
        # myclient.record(_path, _fname, test)
    except:
        raise HTTPException(status_code=400, detail='File Definition Error')

async def read_save_image(_path: str, \
                          _fname: str, \
                          _file: UploadFile, \
                          test: Optional[Union[None, int]]=None):
    
    logger.info(f"save_image: {_path}/{_fname}")
    try:
        ret = None
        image = Image.open(BytesIO(await _file.read()))
        image.save(f"{_path}/{_fname}")
        ret = np.asarray(image)
    except:
        raise HTTPException(status_code=401, detail='File Definition Error')

    return ret


def save_file(path: str, \
              fname: str, \
              file: UploadFile, \
              test: Optional[Union[None, int]]=None):

    try:
        with open(f"{path}/{fname}", 'wb') as local_temp_file:
            local_temp_file.write(file.file.read())
    except:
        raise HTTPException(status_code=400, detail='File Definition Error')
