import os

VERSION = os.getenv('VERSION', 'v0'),
AUTHOR = os.getenv('AUTHOR', 'kevin')
PATH_DATA = os.getenv('PATH_DATA', './temp')

APP_PORT = int(os.getenv('APP_PORT', 80))
