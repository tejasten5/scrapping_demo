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

COMPANY_NAMES = [
    'Aditya Birla Capital Limited',
    'Aditya Birla Chemicals (Thailand)',
    'Aditya Birla Fashion and Retail Limited',
    'Aditya Birla Grasun Chemicals (Fangchenggang)',
    'Aditya Birla Insulators',
    'Aditya Birla Science and Technology Company Private Limited',
    'AV Group NB',
    'Birla Carbon',
    'Birla Jingwei Fibres Company Limited',
    'Dahej Harbour and Infrastructure Limited',
    'Domsjö Fabriker',
    'Essel Mining & Industries Limited',
    'Grasim Industries Limited',
    'Hindalco Industries Limited',
    'Hindalco-Almex Aerospace Limited',
    'Indo Phil Group of Companies',
    'Indo Phil Textile Mills',
    'Indo Thai Synthetics Company Limited',
    'Novelis Inc',
    'PT Elegant Textile Industry (Indonesia)',
    'PT Indo Bharat Rayon (Indonesia)',
    'PT Indo Liberty Textiles (Indonesia)',
    'PT Indo Raya Kimia (Indonesia)',
    'PT Sunrise Bumi Textiles (Indonesia)',
    'Swiss Singapore Overseas Enterprises Pte Ltd',
    'Tanfac Industries Limited',
    'Terrace Bay Pulp Mill',
    'Thai Acrylic Fibre Co. Ltd',
    'Thai Peroxide Company Limited',
    'Thai Rayon',
    'UltraTech Cement Limited',
    'Utkal Alumina International Limited',
    'Vodafone Idea Limited'
]

class LinkdinHeaders:
    LD_DESIGNATION = 'Designation'    
    LD_NAME = 'Name'

class ScrapLinkdinJobs:
    LINKDIN_LOGIN_URL = "https://www.linkedin.com/login"
    FILE_NAME = "linkdin_profiles.csv"    
    LINKDIN_PROFILE_SEARCH_URL = 'https://www.linkedin.com/search/results/people/?keywords={company_name}&sid=ZR%2C'

    def __init__(self,area_of_search=None):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())    

    def linkdin_login(self):  
        self.driver.get(self.LINKDIN_LOGIN_URL)
        time.sleep(5)

        soup=BeautifulSoup(self.driver.page_source, 'lxml')
        username     = self.driver.find_element(By.ID,"username")
        username.send_keys(os.environ.get('USER_EMAIL'))

        pword = self.driver.find_element(By.ID,"password")
        pword.send_keys(os.environ.get('USER_PASSWORD'))		
        self.driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(3)

        self.scrap_profile_data()

        time.sleep(5)
        self.driver.close()

    def scrap_profile_data(self):           

        with open(self.FILE_NAME, 'a',encoding="utf-8") as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=[LinkdinHeaders.LD_DESIGNATION, LinkdinHeaders.LD_NAME])
            dict_object.writeheader()

            for start in range(1,501):
                context = {}               
                import pdb;pdb.set_trace()
                # currentCompany=%5B"1362039"%5D&keywords=neosoft&origin=FACETED_SEARCH&sid=tg%3A&title=CEO
                # https://www.linkedin.com/search/results/people/?currentCompany=%5B%221362039%22%5D&heroEntityKey=urn%3Ali%3Aorganization%3A1362039&keywords=neosoft&origin=FACETED_SEARCH&position=0&searchId=82952b0f-fe4d-4809-ba18-e4408731a5de&sid=lTD&title=CTO
                time.sleep(3)
                URL = f"{self.LINKDIN_PROFILE_SEARCH_URL}"    
                
                self.driver.get(URL)

                time.sleep(10)
                
                try:
                    full_name = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[2]/div/div[2]/div[1]/div/div[4]/section/section/div[1]/div[2]').text.split()[0]
                except Exception as e:
                    full_name = "NA"               
                

                try:
                    designation = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a/h2').text         
                except Exception as e:
                    designation = "NA"   

                


                context.update({LinkdinHeaders.LD_DESIGNATION:designation,LinkdinHeaders.LD_NAME:full_name})
                dict_object.writerow(context)
                time.sleep(10)          
        

logging.warning("{0} Program start time...".format(time.time()))
area_of_search = "php"
ScrapLinkdinJobs(area_of_search).linkdin_login()
logging.warning("{0} Execution completed...".format(time.time()))
