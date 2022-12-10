from setuptools import setup, find_packages
from typing import List
import pathlib
# print(pathlib.Path(__file__).parent)


print(find_packages())

def get_install_requires() -> List[str]:
    """Returns requirements.txt parsed to a list"""
    fname = pathlib.Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(
    name='MediaHandler',\
    version="v0.0.1",\
    url='https://github.com/kevin-tofu/MediaHandler',\
    download_url='https://github.com/kevin-tofu/MediaHandler/releases/tag/v0.0.1',\
    description="",\
    install_requires=get_install_requires(),
    packages=['MediaHandler'],\
    # packages=find_packages(), \
    package_dir = {'MediaHandler': 'MediaHandler'},\
    author='kevin-tofu',\
    license='MIT', \
    python_requires='>3.8'
)
