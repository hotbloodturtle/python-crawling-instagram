import os
import sys
import time
import urllib.request
import random
import string
import glob

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# images 폴더 경로 지정, 없으면 생성
IMAGES_DIR = '../photo/crawling/images/'
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# movies 폴더 경로 지정, 없으면 생성
MOVIES_DIR = '../photo/crawling/movies/'
if not os.path.exists(MOVIES_DIR):
    os.makedirs(MOVIES_DIR)

# 신규계정 txt 파일모음 폴더경로 지정, 없으면 생성
NEW_LIST_DIR = './new_list/'
if not os.path.exists(NEW_LIST_DIR):
    os.makedirs(NEW_LIST_DIR)

# 기존 계정 txt 파일모음 폴더경로 지정, 없으면 생성
EXISTING_LIST_DIR = './existing_list/'
if not os.path.exists(EXISTING_LIST_DIR):
    os.makedirs(EXISTING_LIST_DIR)

# os환경에 맞게 크롬드라이버 경로 세팅, os.name == 'nt'면 windows
if os.name == 'nt':
    DRIVER_DIR = './chromedriver/chromedriver.exe'
else:
    DRIVER_DIR = './chromedriver/chromedriver'

# random으로 파일 문자열 생성 메서드
def create_file_name():
    val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return val
