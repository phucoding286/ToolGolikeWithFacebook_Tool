import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle

import copy
import time
import colorama
import json
import os
import sys
import datetime
colorama.init()

# input(datetime.datetime.today().day)

def driver_init(chrome_user_data=None):
    options = webdriver.ChromeOptions() 
    options.add_argument("--log-level=3")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-position=1050,0")

    if chrome_user_data is not None:
        options.add_argument(f"--user-data-dir={chrome_user_data}")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(50, 500)
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