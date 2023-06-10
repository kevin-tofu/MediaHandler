import os
from typing import Optional, Union
from mediarouter.logconf import medialogger
logger = medialogger(__name__)
print('__name__', __name__)
from fastapi import HTTPException


def video_conversion(
    path_file_src: str,
    path_file_dst: str,
    test: Optional[Union[None, int]]=None
):
    
    import ffmpeg

    if test is None:
        stream = ffmpeg.input(path_file_src, v="quiet")
        stream = ffmpeg.output(stream, path_file_dst, v="quiet")
    else:
        stream = ffmpeg.input(path_file_src)
        stream = ffmpeg.output(stream, path_file_dst)
    ffmpeg.run(stream)


def video_conversion_fname(
    path_data: str, 
    fname_src: str, 
    fname_dst: str
):

    video_conversion(
        f"{path_data}/{fname_src}",
        f"{path_data}/{fname_dst}"
    )


def video_conversion_xxx2mp4(
    path_data: str,
    fname: str,
    remove_fileorg : bool=True
):
# def converter_xxx2mp4(path_data: str, fname: str):

    fname_without_ext = os.path.splitext(fname)[0]
    fname_dst = f'{fname_without_ext}.mp4'

    file_ext = os.path.splitext(fname)[-1]
    if file_ext == ".mp4" or file_ext == ".MP4":
        return fname
    else:
        video_conversion_fname(path_data, fname, fname_dst)
        if os.path.exists(f"{path_data}/{fname}") and remove_fileorg:
            os.remove(f"{path_data}/{fname}")

        return fname_dst


def is_same_extension_file(
    fname1: str,
    fname2: str
):
    """
    """

    file1_ext = os.path.splitext(fname1)[-1]
    file2_ext = os.path.splitext(fname2)[-1]
    if file1_ext == file2_ext or \
       file1_ext == file2_ext.upper() or \
       file1_ext == file2_ext.lower():
        return True
    else:
        return False

def get_extension(fname: str):
    
    file_org_ext = os.path.splitext(fname)[-1]
    return file_org_ext[1::]

def is_same_extension(
    fname: str,
    extension: str
):
    """
    """

    file_org_ext = get_extension(fname)
    if file_org_ext == f"{extension}" or file_org_ext == f"{extension.upper()}":
    # if file_org_ext == f".{extension}" or file_org_ext == f".{extension.upper()}":
        return True
    else:
        return False


def video_conversion_xxx2yyy(
    path_data: str,
    fname: str,
    yyy: str = 'mp4',
    remove_fileorg : bool=True
):
    """
    """

    fname_without_ext = os.path.splitext(fname)[0]
    fname_dst = f'{fname_without_ext}.{yyy}'

    file_org_ext = os.path.splitext(fname)[-1]
    if is_same_extension(file_org_ext, yyy):
        # if extension is as same as original, do nothing
        # shutil.copy2()
        return fname
    else:
        video_conversion_fname(path_data, fname, fname_dst)
        if os.path.exists(f"{path_data}/{fname}") and remove_fileorg:
            os.remove(f"{path_data}/{fname}")

        return fname_dst


def set_audio(path_src, path_dst):
    """
    https://kp-ft.com/684
    https://stackoverflow.com/questions/46864915/python-add-audio-to-video-opencv
    """

    import os, shutil
    import moviepy.editor as mp
    import time

    root_ext_pair = os.path.splitext(path_src)
    path_dst_copy = f"{root_ext_pair[0]}-copy{root_ext_pair[1]}"
    shutil.copyfile(path_dst, path_dst_copy)
    time.sleep(0.5)

    # Extract audio from input video.                                                                     
    clip_input = mp.VideoFileClip(path_src)
    # clip_input.audio.write_audiofile(path_audio)
    # Add audio to output video.                                                                          
    clip = mp.VideoFileClip(path_dst_copy)
    clip.audio = clip_input.audio

    time.sleep(0.5)
    clip.write_videofile(path_dst)

    time.sleep(0.5)
    os.remove(path_dst_copy)


def xxx2mp4(self, path_data: str, fname: str):
    """
    """
    fname_noext = os.path.splitext(fname)[0]
    fname_dst = f'{fname_noext}.mp4'
    file_ext = os.path.splitext(fname)[-1]
    if file_ext == ".mp4" or file_ext == ".MP4":
        return fname
    else:
        video_conversion_xxx2yyy(
            path_data,
            fname,
            fname_dst,
            remove_fileorg=True
        )
        return fname_dst


def save_video(
    path: str,
    fname: str,
    file: UploadFile,
    test: Optional[Union[None, int]]=None
):

    logger.debug("save_video")
    try:
        with open(f"{path}/{fname}", 'wb') as local_temp_file:
            local_temp_file.write(file.file.read())
    except:
        raise HTTPException(status_code=400, detail='File Definition Error')


