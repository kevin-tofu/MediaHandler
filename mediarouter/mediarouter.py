
import os, sys
from typing import List, Union, Dict, Optional
import time
import zipfile

from fastapi.responses import FileResponse, JSONResponse
from fastapi import HTTPException, BackgroundTasks
from fastapi import Response, UploadFile
# import numpy as np
import io
import cv2

from mediarouter.logconf import medialogger
logger = medialogger(__name__)
print('__name__', __name__)
from mediarouter import tools


class Config():
    def __init__(self, **kwargs):

        print("kwargs: ", kwargs)
        self.path_data = kwargs["PATH_DATA"] if "PATH_DATA" in kwargs.keys() else "./temp"
        self.image_extensions = kwargs["EXTENSIONS_IMAGE"] if "EXTENSIONS_IMAGE" in kwargs.keys() else ["jpg", "png", "tiff"]
        self.video_extensions = kwargs["EXTENSIONS_VIDEO"] if "EXTENSIONS_VIDEO" in kwargs.keys() else ["mp4", "avi", "webm", "wmv", "flv"]
        # self.sleep_sec_remove = _config.SLEEP_SEC_REMOVE
        # self.sleep_sec_remove_response = _config.SLEEP_SEC_REMOVE_RESPONSE


class Processor():

    def __init__(self, **kwargs):
        pass
    
    async def post_files_process(
        self, \
        process_name: str, \
        fpath_files: List[str], \
        fpath_dst: Optional[str] = None, \
        bgtask: BackgroundTasks=BackgroundTasks(), \
        **kwargs
    ):
        raise NotImplementedError()

    async def post_file_process(
        self, \
        process_name: str, \
        fpath_org: str, \
        fpath_dst: Optional[str] = None, \
        bgtask: BackgroundTasks=BackgroundTasks(), \
        **kwargs
    ):

        raise NotImplementedError()

    async def post_BytesIO_process(
        self, \
        process_name: str, \
        fBytesIO: io.BytesIO, \
        fname_org: str, \
        **kwargs
    ):
        raise NotImplementedError()


class Router():
    def __init__(
        self, \
        processor: Processor, \
        config: Config
    ):

        self.processor = processor
        self.config = config
        self.path_data = config.path_data
        os.makedirs(self.path_data, exist_ok=True)
        

    def is_processable_image_ext(self, fname: str):
        return tools.get_file_extension(fname).lower() in self.image_extensions
    
    def is_processable_video_ext(self, fname: str):
        return tools.get_file_extension(fname).lower() in self.video_extensions


    def post_processing(self, fpath_dst: str, **kwargs):

        ftype_dst = tools.check_filetype(fpath_dst)
        fname = os.path.basename(fpath_dst)
        ext = tools.get_file_extension(fpath_dst)
        # print(ftype_dst, ext, tools.FileType.IMAGE)
        # print(ftype_dst == tools.FileType.IMAGE)
        if ftype_dst == tools.FileType.IMAGE:
            img = cv2.imread(fpath_dst)
            _, img = cv2.imencode(f'.{ext}', img)
            return Response(
                img.tostring(), \
                media_type = f'image/{ext}', \
                # filename=fname
                # background=bgtask
            )
        
            # _, image_enc = cv2.imencode(f'.{ext}', img)
            
            # return Response(content = image_enc.tostring(), \
            #                 media_type = f'image/{ext}', \
            #                 background=bgtask
            # )
        else:
            return FileResponse(
                fpath_dst, \
                filename=f"{fname}", \
                media_type = f'video/{ext}'
                # background=bgtask
            )

    async def post_files(
        self, \
        process_name: str, \
        files_list: List[UploadFile], \
        retfile_extension: Optional[str] = None, \
        bgtask: BackgroundTasks = BackgroundTasks(),\
        **kwargs
    ):

        logger.info("post_files")
        test = kwargs['test']
        kwargs['bgtask'] = bgtask
        
        try:
        # if True:

            path_files_list = list()
            fname_list = list()
            fname_org_list = list()
            for file in files_list:

                logger.info(f'{file.filename}, {file.content_type}')

                fname_org = file.filename
                fname, uuid_f = tools.fname2uuid(fname_org)
                tools.save_file(self.path_data, fname, file, test)

                fname_list.append(fname)
                path_files_list.append(f"{self.path_data}/{fname}")
                fname_org_list.append(fname_org)
            
            kwargs["fname_org_list"] = fname_org_list
            bgtask.add_task(tools.remove_files, path_files_list)

            if not retfile_extension is None:
                fname_dst = tools.make_fname_uuid(retfile_extension)
                fpath_dst = f"{self.path_data}/{fname_dst}"
                bgtask.add_task(tools.remove_file, fpath_dst)
            else:
                fpath_dst = None


            result = await self.processor.post_files_process(
                process_name, \
                path_files_list, \
                fpath_dst, \
                **kwargs
            )
            
            if type(fpath_dst) is str:
                if os.path.exists(fpath_dst):
                    return self.post_processing(fpath_dst, **kwargs)
                else:
                    return result
            else:
                return result
            
        # try:
        #     pass
        except:
            raise HTTPException(status_code=503, detail="Error") 
        finally:
            # print("finally0")
            pass
        
        
    def preprocess_zip(self, fname, bgtask):
        path_dir_export = f"{self.path_data}/{os.path.splitext(fname)[0]}"
        os.makedirs(path_dir_export)
        bgtask.add_task(tools.remove_dir, path_dir_export)
        with zipfile.ZipFile(f"{self.path_data}/{fname}") as zf:
            zf.extractall(path = path_dir_export)
        bgtask.add_task(tools.remove_dir, path_dir_export)

    async def post_file(
        self, \
        process_name: str, \
        file: UploadFile, \
        retfile_extension: Optional[str] = None, \
        bgtask: BackgroundTasks = BackgroundTasks(),\
        **kwargs
    ):

        logger.info("post_file")
        kwargs['bgtask'] = bgtask

        # try:
        if True:
            test = kwargs["test"]

            fname_org = file.filename
            ftype_input = tools.check_filetype(fname_org)
            fname, uuid_f = tools.fname2uuid(fname_org)
            tools.save_file(self.path_data, fname, file, test)
            kwargs["fname_org"] = fname_org

            bgtask.add_task(tools.remove_file, f"{self.path_data}/{fname}")
            if ftype_input == tools.FileType.ZIP:
                self.preprocess_zip(fname, bgtask)
                
            if not retfile_extension is None:
                fname_dst = tools.addstr2fname(fname, "-res", ext = retfile_extension)
                fpath_dst = f"{self.path_data}/{fname_dst}"
                bgtask.add_task(tools.remove_file, fpath_dst)
            else:
                fpath_dst = None

            result = await self.processor.post_file_process(
                process_name, \
                f"{self.path_data}/{fname}", \
                fpath_dst, \
                **kwargs
            )
            
            if type(fpath_dst) is str:
                if os.path.exists(fpath_dst):
                    return self.post_processing(fpath_dst, **kwargs)
                else:
                    return result
            else:
                return result

        try:
            pass
        except:
            raise HTTPException(status_code=503, detail="Error") 
        finally:
            # print("finally0")
            pass
        

    async def post_file_BytesIO(
        self, \
        process_name: str, \
        file: UploadFile, \
        bgtask: BackgroundTasks = BackgroundTasks(),\
        **kwargs
    ):

        logger.info("post_file_BytesIO")
        kwargs['bgtask'] = bgtask

        if kwargs['test'] == 1:
            test = kwargs["test"]

            fname_org = file.filename
            file_byte = io.BytesIO(await file.read())
            ftype_input = tools.check_filetype(fname_org)

            result = await self.processor.post_BytesIO_process(
                process_name, \
                file_byte, \
                fname_org, \
                **kwargs
            )
            return result
        else:
            try:
            # if True:
                test = kwargs["test"]

                fname_org = file.filename
                file_byte = io.BytesIO(await file.read())
                ftype_input = tools.check_filetype(fname_org)

                result = await self.processor.post_BytesIO_process(
                    process_name, \
                    file_byte, \
                    fname_org, \
                    **kwargs
                )
                return result
                
            # try:
            #     pass
            except:
                raise HTTPException(status_code=503, detail="Error") 
            finally:
                # print("finally0")
                pass
                
