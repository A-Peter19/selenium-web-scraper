from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Paths to your drivers and Brave browser
driver_path = r"D:\02_personal\WH-data\Neighbourly-automation\chrome-win64\chromedriver.exe"
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# Setup ChromeOptions to use Brave instead
options = webdriver.ChromeOptions()
options.binary_location = brave_path  # Tell Selenium to launch Brave

driver = webdriver.Chrome(executable_path=driver_path, options=options)  # Like Chrome, but uses Brave
