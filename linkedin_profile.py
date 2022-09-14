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
    LD_FIRST_NAME = 'First Name'
    LD_LAST_NAME = 'Last Name'
    LD_COMPANY_NAME = 'Company Name'
    LD_DESIGNATIONS = 'Designation'
    LD_COUNTRIES = "Country"
    LD_CITIES = "City"
    LD_URLS = 'URL'
    

class ScrapLinkdinJobs:
    LINKDIN_LOGIN_URL = "https://linkedin.com/uas/login"
    FILE_NAME = "linkdin_profile.csv"
    HEADERS_LIST = [
        LinkdinHeaders.LD_FIRST_NAME,
        LinkdinHeaders.LD_LAST_NAME,
        LinkdinHeaders.LD_COMPANY_NAME,
        LinkdinHeaders.LD_DESIGNATIONS,
        LinkdinHeaders.LD_COUNTRIES,
        LinkdinHeaders.LD_CITIES,
        LinkdinHeaders.LD_URLS,

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
        # with open(self.FILE_NAME, 'a',encoding="utf-8") as csv_file:
        #     dict_object = csv.DictWriter(csv_file, fieldnames=self.HEADERS_LIST)
        #     dict_object.writeheader()
        #     context = {}
        filter_designation = ["VP","VP IT","CIO" ,"CTO","CISO","Director IT","Head IT- (Technology)","Procurement Director","Manager","Head","CHRO","HR Manager","HR Director","VP HR","Head HR"]
        urls = []
        first_name_l,last_name_l = [],[]
        company_name = []
        designations = []
        countries = []
        cities = []

        for filter in filter_designation:
            for i in range(1,500):
                URL = 'https://www.linkedin.com/search/results/people/?company=aditya-birla-capital&page='+str(i)+'&title='+filter
                self.driver.get(URL)

                time.sleep(10)
                soup=BeautifulSoup(self.driver.page_source, 'lxml')
        # all_links = []
        # elements = self.driver.find_elements(By.XPATH,'//*[@id="main"]/div/div/div[1]/ul/li')
        # print(len(elements))
        # all_links.append(elements)
        # print("all_links===>>>",all_links)
        
        # for x in all_links:
                if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                    break

                all_names=self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[1]/div/span[1]/span/a')
                for name in all_names:
                    n = name.text.split()
                # print(n[0])
                    try:
                        first_name_l.append(n[0])
                        first_name=n[0]
                    except:
                        first_name_l.append('NA')
                # print(n[1])
                    try:
                        last_name_l.append(n[1])
                        last_name=n[0]
                    except:
                        last_name_l.append("NA")

            
                try:
                    for i in range(1,len(all_names)+1):
            # print("neosoft")
                        a="aditya-birla-capital"
                        company_name.append(str(a))
                except:
                    company_name.append(str(a))

            
                try:
                    all_designations=self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[2]/div/div[1]')
                    for designation in all_designations:
            # print(designation.text)if designation in filter_degisnation:
                        designations.append(designation.text)
                except:
                    designations.append("NA")


            
                try:
                    for i in range(1,len(all_names)+1):
            # print("India")
            # b = "India"
                        countries.append("India")
                except:
                    countries.append("NA")

            
                try:
                    all_cities = self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[2]/div/div[2]')
                    for city in all_cities:
            # print(city.text)
                        cities.append(city.text)
                except:
                    cities.append("NA")

            
                try:
                    linkedin_url = self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[1]/div/span/span/a')
                    for url in linkedin_url:
            # print(url.get_attribute("href").split('?')[0])
                        u = url.get_attribute("href").split('?')[0]

                        urls.append(u)
                except:
                    urls.append("NA")
        
                print(first_name_l)
                print(last_name_l)
                print(company_name)
                print(designations)
                print(countries)
                print(cities)
                print(urls)
                print("hi==========>>>>>>>>>>>>>")
                time.sleep(5)

        

        df=pd.DataFrame()
        df['Firstname'] = pd.Series(first_name_l)
        df['Lastname'] = last_name_l
        df['Company']=pd.Series(company_name)
        df['Designation']=pd.Series(designations)
        df['Country']=pd.Series(countries)
        df['City']=pd.Series(cities)
        df['URL']=pd.Series(urls)
        df.to_csv(self.FILE_NAME,index=False)
        # df['City']
        # self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[3]/div/div/button[2]/span')

 
logging.warning("{0} Program start time...".format(time.time()))
ScrapLinkdinJobs().linkdin_login()
logging.warning("{0} Execution completed...".format(time.time()))
