from setuptools import setup, find_packages

print(find_packages())
setup(
    name='MediaHandler',\
    version="0.0.1",\
    url='https://github.com/kevin-tofu/MediaHandler',\
    download_url='https://github.com/kevin-tofu/MediaHandler/releases/tag/v0.0.1',\
    description="",\
    packages=['MediaHandler'],\
    # packages=find_packages(), \
    package_dir = {'MediaHandler': 'MediaHandler'},\
    author='kevin-tofu',\
    license='MIT', \
)
