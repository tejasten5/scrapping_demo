from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os
from dotenv import load_dotenv
import csv
load_dotenv()


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://linkedin.com/uas/login")
time.sleep(5)
soup=BeautifulSoup(driver.page_source, 'lxml')

username = driver.find_element(By.ID,"username")
# Enter Your Email Address
username.send_keys(os.environ.get('USER_EMAIL'))
pword = driver.find_element(By.ID,"password")
# Enter Your Password
pword.send_keys(os.environ.get('USER_PASSWORD'))		
driver.find_element(By.XPATH,"//button[@type='submit']").click()
time.sleep(3)


links = []
designation_l,company_l,location_l,post_date_l=[],[],[],[]
job_type_l,employees_l,description_l,seperator_l=[],[],[],[]
url_l,post_by_l,post_designation_l=[],[],[]

area_of_search = "python"
location = "india"

class LinkdinCSVHeaders:
   LD_DESIGNATION = 'Designation'
   LD_COMPANY_NAME = 'Company Name'
   LD_LOCATION = 'Location'
   LD_POST_DATE = 'Post Date'
   LD_JOB_TYPE = 'Job Type'
   LD_EMPLOYEE = 'Employees'
   LD_JOB_DESCRIPTION = 'Job Description'
   LD_URL = 'URL'
   LD_POST_BY = 'Post By'
   LD_POST_DESIGNATION  = 'Post Designation'


HEADERS_LIST = [
    LinkdinCSVHeaders.LD_DESIGNATION,
    LinkdinCSVHeaders.LD_COMPANY_NAME,
    LinkdinCSVHeaders.LD_LOCATION,
    LinkdinCSVHeaders.LD_POST_DATE,
    LinkdinCSVHeaders.LD_JOB_TYPE,
    LinkdinCSVHeaders.LD_EMPLOYEE,
    LinkdinCSVHeaders.LD_JOB_DESCRIPTION,
    LinkdinCSVHeaders.LD_URL,
    LinkdinCSVHeaders.LD_POST_BY,
    LinkdinCSVHeaders.LD_POST_DESIGNATION
]


with open("test.csv", 'a') as csv_file:
    dict_object = csv.DictWriter(csv_file, fieldnames=HEADERS_LIST)
    dict_object.writeheader()

    
        
    for start in range(1,6):
        context = {}

        time.sleep(10)
        # URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3103152586&geoId=102713980&keywords=python&location=India&refresh=true'
        URL = "https://www.linkedin.com/jobs/search/?keywords="+area_of_search+"&location="+location+"&start="+str(start)+"&refresh=True"
        print(URL,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        driver.get(URL)
        # time.sleep(10)

        designation = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a/h2').text        
        company=driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/span/span').text
        location=driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/span/span[2]').text
        post_date = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/span[2]/span').text

        time.sleep(3)

        job_type = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/ul/li[1]/span').text
        employees = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[2]/ul/li[2]/span').text
       
        time.sleep(3)
                
        description = driver.find_element(By.XPATH,'//*[@id="job-details"]/span').text        

        time.sleep(2)

        url =driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/span/span/a').get_attribute('href')       

        try:
            post_by = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/a').text            
        except:
            post_by = "NA"            

        try:
            post_designation = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div')           
        except:           
            post_designation = "NA"           


        context.update({
                'Designation':designation,
                'Company Name':company,
                'Location':location,
                'Post Date':post_date,
                'Job Type':job_type,
                'Employees':employees,
                'Job Description':description,
                'URL':url,
                'Post By':post_by,
                'Post Designation':post_designation
        })
        print(context,">>>>>>>>>>>>>>>>>>>>>>>>>>>>") 
        dict_object.writerow(context)
        time.sleep(10)  

        
    
    
        

FILE_NAME = 'scrap_linkedin.csv'           
driver.close()
