import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pickle
import shutil

import copy
import time
import colorama
import json
import os
import sys
import datetime
import cloudscraper
import random
import requests
from selenium.webdriver.common.action_chains import ActionChains
colorama.init()

def driver_init(chrome_user_data=None, hide_chrome=False):
    options = webdriver.ChromeOptions() 
    options.add_argument("--log-level=3")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--window-size=1920,1080')

    # đảm bảo chrome vẫn render hình ảnh dù bị ẩn
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=PaintHolding")
    options.add_argument("--disable-features=FreezeUserAgent")

    if hide_chrome:
        options.add_argument('--window-position=0,10000')

    if chrome_user_data is not None:
        options.add_argument(f"--user-data-dir={chrome_user_data}")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    return driver

# make color for logs
def error_color(string: str):
    return colorama.Fore.RED + str(string) + colorama.Style.RESET_ALL
def success_color(string: str):
    return colorama.Fore.GREEN + str(string) + colorama.Style.RESET_ALL
def system_color(string: str):
    return colorama.Fore.YELLOW + str(string) + colorama.Style.RESET_ALL
def wait_color(string: str):
    return colorama.Fore.BLUE + str(string) + colorama.Style.RESET_ALL
def purple_color(string: str):
    return colorama.Fore.MAGENTA + str(string) + colorama.Style.RESET_ALL


# make waiting animation theme
def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(colorama.Fore.YELLOW + f"\r[{i}s] " + colorama.Style.RESET_ALL, end="")
        print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0

def facebook_login(driver):
    driver.get("https://www.facebook.com/")
    input(system_color("[?] Hãy nhập username và mật khẩu của bạn và nhấn đăng nhập\n-> "))

def golike_login(driver):
    driver.get("https://app.golike.net/")
    input(system_color("[?] Hãy nhập username và mật khẩu của bạn và nhấn đăng nhập\n-> "))

def golike_job_setup(driver):
    driver.get("https://app.golike.net/jobs/facebook?load_job=true")
    input(system_color("[?] Hãy setup tài khoản cần làm việc\n-> "))