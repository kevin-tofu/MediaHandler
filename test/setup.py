from setuptools import setup, find_packages
from typing import List
import pathlib
import os
# print(pathlib.Path(__file__).parent)


print(find_packages())

def get_install_requires() -> List[str]:
    """Returns requirements.txt parsed to a list"""
    fpath = f"{pathlib.Path(__file__).parent}/requirements.txt"
    targets = []
    print(fpath)
    if os.path.exists(fpath):
        with open(fpath, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(
    name='MediaRouter',\
    version="v0.0.1",\
    url='https://github.com/kevin-tofu/MediaRouter',\
    download_url='https://github.com/kevin-tofu/MediaRouter/releases/tag/v0.0.1',\
    description="",\
    install_requires=get_install_requires(),
    # install_requires=['fastapi', 'uvicorn', 'wheel'],
    packages=['MediaRouter'],\
    # packages=find_packages(), \
    package_dir = {'MediaRouter': 'MediaRouter'},\
    author='kevin-tofu',\
    license='MIT', \
    python_requires='>3.8'
)
