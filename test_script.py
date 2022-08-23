# Install selenium using command " pip install selenium "

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import csv

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 20)

print(">>>")
URL = '''https://www.naukri.com/python-jobs?k=python'''
driver.get(URL)

XPATH = '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article'
# import pdb;pdb.set_trace()

elements = driver.find_elements(By.XPATH, XPATH)     

# for idx in range(1,20):
#     time.sleep(1) 
#     wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[{idx}]'))).click()
#     time.sleep(1) 




