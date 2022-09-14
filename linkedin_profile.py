from lib2to3.pgen2 import driver
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os,csv,time,logging
from dotenv import load_dotenv
load_dotenv()
 
# USER_EMAIL 
# USER_PASSWORD 

class LinkdinHeaders:
    LD_DESIGNATION = 'Designation'
    LD_COMPANY_NAME = 'Company Name'
    LD_LOCATION = 'Location'
    LD_POST_DATE = 'Post Date'
    LD_POST_TYPE = 'Job Type'
    LD_EMPLOYEES = 'Employees'
    LD_JOB_DESCRIPTION = 'Job Description'
    LD_URL = 'URL'
    LD_POST_BY = 'Post By'
    LD_POST_DESIGNATION = 'Post Designation'
    LD_INDUSTRY_TYPE = 'Industry'

class ScrapLinkdinJobs:
    LINKDIN_LOGIN_URL = "https://linkedin.com/uas/login"
    FILE_NAME = "linkdin_jobs.csv"
    HEADERS_LIST = [
        LinkdinHeaders.LD_DESIGNATION,
        LinkdinHeaders.LD_COMPANY_NAME,
        LinkdinHeaders.LD_LOCATION,
        LinkdinHeaders.LD_POST_DATE,
        LinkdinHeaders.LD_POST_TYPE,
        LinkdinHeaders.LD_EMPLOYEES,
        LinkdinHeaders.LD_JOB_DESCRIPTION,
        LinkdinHeaders.LD_URL,
        LinkdinHeaders.LD_POST_BY,
        LinkdinHeaders.LD_POST_DESIGNATION,
        # LinkdinHeaders.LD_INDUSTRY_TYPE
    ]

    def __init__(self,area_of_search=None,location=None):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())    

    def linkdin_login(self):  
        self.driver.get(self.LINKDIN_LOGIN_URL)
        time.sleep(5)

        soup=BeautifulSoup(self.driver.page_source, 'lxml')
        username = self.driver.find_element(By.ID,"username")
        username.send_keys(os.environ.get('USER_EMAIL'))

        pword = self.driver.find_element(By.ID,"password")
        pword.send_keys(os.environ.get('USER_PASSWORD'))		
        self.driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(3)

        self.scrap_linkdin_jobs()

        time.sleep(5)
        self.driver.close()

    def scrap_linkdin_jobs(self):  
        URL = 'https://www.linkedin.com/search/results/people/?company=neosoft&title=VP'
        self.driver.get(URL)

        time.sleep(10)

        # all_links = []
        # elements = self.driver.find_elements(By.XPATH,'//*[@id="main"]/div/div/div[1]/ul/li')
        # print(len(elements))
        # all_links.append(elements)
        # print("all_links===>>>",all_links)
        
        # for x in all_links:
        
        all_names=self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]')
        for name in all_names:
            n = name.text.split()
            print(n[0])
            print(n[1])

        for i in range(1,len(all_names)+1):
            print("neosoft")

        all_designations=self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[2]/div/div[1]')
        for designation in all_designations:
            print(designation.text)

        for i in range(1,len(all_names)+1):
            print("India")

        all_cities = self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[2]/div/div[2]')
        for city in all_cities:
            print(city.text)

        # s = self.driver.find_element(By.CLASS_NAME,'entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light').text
        # print(s)

# //*[@id="main"]/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[1]
# //*[@id="main"]/div/div/div[1]/ul/li[2]/div/div/div[2]/div/div[1]
logging.warning("{0} Program start time...".format(time.time()))
ScrapLinkdinJobs().linkdin_login()
logging.warning("{0} Execution completed...".format(time.time()))
