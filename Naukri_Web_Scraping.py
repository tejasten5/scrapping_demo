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

URL = '''https://www.naukri.com/python-jobs?k=python'''
FILE_NAME = 'Naukri_scrape.csv'
FILE_MODE = 'a'
CSV_HEADERS = ['Designation', 'Company name', 'URL', 'Experience', 'Salary','Description','Job Description']

old_url = 'https://www.naukri.com/jobs-in-chennai-1'
# Update the URL of Naukri Page! ( Make Sure that the page link which you're putting must be a job listing page and it must have Next page buttons. )
driver.get(URL)

count = 5  # Update the Number of Vacancy count you want to scrape.

index, new_index, i = '0', 1, 0  # This the the index variable of the elements from which data will be Scraped
# Xpaths of the various element from which data will be scraped.
heading_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])['+index+']/div/div/a'
link_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])['+index+']/div/div/a'
subheading_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])['+index+']/div/div/div/a'
experience_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])['+index+']/div/div/ul/li[1]/span'
salary_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])['+index+']/div/div/ul/li[2]/span'
job_description_xpath = '(//*[@class="jobTuple bgWhite br4 mb-8"])['+index+']/div/div/ul/li[3]/span'

# for_details_page= '(//*[@class="jobTuple bgWhite br4 mb-8"])'
# driver.find_element('(//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[1]/div[1]').click()
# time.sleep(10)
# wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[1]/div[1]'))).click()

time.sleep(10)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[1]/div[1]'))).click()
time.sleep(10)


# csv_file = open(FILE_NAME, FILE_MODE, encoding="utf-8", newline='')
# csv_writer = csv.writer(csv_file)
# # Writing the Heading of CSV file.
# csv_writer.writerow(CSV_HEADERS)

# while i < count:

#     for j in range(20):
#         # Here we're replacing the Old index count of Xpath with New Index count.
#         temp_index = str(new_index).zfill(2)  # Zfill(2) is used to put zeros to the left of any digit till 2 decimal places.
#         heading_xpath = heading_xpath.replace(index, temp_index)
#         link_xpath = link_xpath.replace(index, temp_index)
#         subheading_xpath = subheading_xpath.replace(index, temp_index)
#         experience_xpath = experience_xpath.replace(index, temp_index)
#         salary_xpath = salary_xpath.replace(index, temp_index)
#         job_description_xpath = job_description_xpath.replace(index, temp_index)

#         index = str(new_index).zfill(2)
#         try:
#             # Capturing the Heading from webpage and storing that into Heading variable.
#             heading = wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath))).text
#             print(heading)
#         except:
#             heading = "NULL"
#         try:
#             link = wait.until(EC.presence_of_element_located((By.XPATH, link_xpath))).get_attribute('href')
#             print(link)
#         except:
#             link = "NULL"
#         try:
#             subheading = wait.until(EC.presence_of_element_located((By.XPATH, subheading_xpath))).text
#             print(subheading)
#         except:
#             subheading = "NULL"
#         try:
#             experience = wait.until(EC.presence_of_element_located((By.XPATH, experience_xpath))).text
#             print(experience)
#         except:
#             experience = "NULL"
#         try:
#             salary = wait.until(EC.presence_of_element_located((By.XPATH, salary_xpath))).text
#             print(salary)
#         except:
#             salary = "Not Disclosed"

#         try:
#             job_description = wait.until(EC.presence_of_element_located((By.XPATH, job_description_xpath))).text
#             print(job_description)
#         except:
#             job_description = "NA"
#         new_index += 1
#         i += 1
#         print("--------------------------- "+str(i)+" ----------------------------------")
#         # Writing all the Scrapped data into CSV file.
#         csv_writer.writerow([heading, subheading, link, experience, salary,job_description])
#         if i >= count:
#             break
#     if i >= count:
#         break
#     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text() = "Next"]'))).click()
#     new_index = 1
# csv_file.close()
