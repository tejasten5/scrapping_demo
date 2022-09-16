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
    NEW_FILE_NAME = "filter_profile.csv"
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

        companies = ["aditya-birla-capital"]
        filter_designation = ["VP IT","CTO","Director IT","Head IT -(Technology)","VP-IT","Vice President - IT"]
        
        urls = []
        first_name_l,last_name_l = [],[]
        company_name = []
        designations = []
        countries = []
        cities = []

        for company in companies:
            for filter in filter_designation:
                for i in range(1,500):
                    URL = 'https://www.linkedin.com/search/results/people/?company='+company+'&page='+str(i)+'&title='+filter
                    self.driver.get(URL)

                    time.sleep(10)
                    soup=BeautifulSoup(self.driver.page_source, 'lxml')
        
                    if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                        break

                    all_names=self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[1]/div/span[1]/span/a')
                    for name in all_names:
                        n = name.text.split()
                
                        try:
                            first_name_l.append(n[0])
                            first_name=n[0]
                        except:
                            first_name_l.append('NA')
                
                        try:
                            last_name_l.append(n[1])
                            last_name=n[0]
                        except:
                            last_name_l.append("NA")

            
                    try:
                        for i in range(1,len(all_names)+1):
            
                            a=company
                            company_name.append(str(a))
                    except:
                        company_name.append(str(a))

            
                    try:
                        all_designations=self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[2]/div/div[1]')
                        for designation in all_designations:
            
                            designations.append(designation.text)
                    except:
                        designations.append("NA")


            
                    try:
                        for i in range(1,len(all_names)+1):
            
            
                            countries.append("India")
                    except:
                        countries.append("NA")

            
                    try:
                        all_cities = self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[2]/div[2]')
                        for city in all_cities:
            
                            cities.append(city.text)
                    except:
                        cities.append("NA")

            
                    try:
                        linkedin_url = self.driver.find_elements(By.XPATH,'//*[@class="entity-result"]/div/div[2]/div[1]/div[1]/div/span/span/a')
                        for url in linkedin_url:
            
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
        df['Firstname'] = pd.Series(first_name_l,dtype='object')
        df['Lastname'] = last_name_l
        df['Company']=pd.Series(company_name,dtype='object')
        df['Designation']=pd.Series(designations,dtype='object')
        df['Country']=pd.Series(countries,dtype='object')
        df['City']=pd.Series(cities,dtype='object')
        df['URL']=pd.Series(urls,dtype='object')
        df.to_csv(self.FILE_NAME,index=False)
        
        # time.sleep(10)
        # read_CSV = pd.read_csv(self.FILE_NAME)
        # filtered_df = read_CSV[read_CSV['Designation'].astype(str).str.contains('VP')|read_CSV['Designation'].astype(str).str.contains('VP IT')|read_CSV['Designation'].astype(str).str.contains('Vice President')|read_CSV['Designation'].str.contains('CIO')|read_CSV['Designation'].str.contains('Chief Information Officer')|read_CSV['Designation'].str.contains('CTO')|read_CSV['Designation'].str.contains('Chief Technology Officer')|read_CSV['Designation'].str.contains('CISO')|read_CSV['Designation'].str.contains('Chief Information Security Officer')|read_CSV['Designation'].str.contains('Director IT')|read_CSV['Designation'].str.contains('Head IT- (Technology)')]
        # time.sleep(10)
        # filtered_df.to_csv(self.NEW_FILE_NAME)
 
logging.warning("{0} Program start time...".format(time.time()))
ScrapLinkdinJobs().linkdin_login()
logging.warning("{0} Execution completed...".format(time.time()))
