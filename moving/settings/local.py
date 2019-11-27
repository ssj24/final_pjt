from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY', default='q!pclg(#j1(zi5(2ft-14pm+slvkn%#fze_t1hn6b4f0!k(&i^')
#.env에서 불러올 시크릿 키가 없을 때 defalut키를 쓰는 것
DEBUG = True

ALLOWED_HOSTS = []