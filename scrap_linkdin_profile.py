from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os,csv,time,logging
from dotenv import load_dotenv
load_dotenv()
 
# create .env file with env variables.
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
    TOTAL_RECORDS_ON_SINGLE_PAGE = 10
    HEADERS_LIST = [
        LinkdinHeaders.LD_FIRST_NAME,
        LinkdinHeaders.LD_LAST_NAME,
        LinkdinHeaders.LD_COMPANY_NAME,
        LinkdinHeaders.LD_DESIGNATIONS,
        LinkdinHeaders.LD_CITIES,
        LinkdinHeaders.LD_URLS,
        LinkdinHeaders.LD_COUNTRIES
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
        
    def fetch_data(self,soup,dict_object,context):
        print("........")
        for html in soup.find(attrs={'class':'reusable-search__entity-result-list list-style-none'}).findAll(attrs={'class':'reusable-search__result-container'}):
            print("-----")
            try:
                profile_url = html.find(attrs={'class':'app-aware-link scale-down'})['href']
            except Exception as e:
                profile_url = "NA"

            try:
                name = html.findAll('span',attrs={'aria-hidden':'true'})[0].get_text()                        
                name_list = name.split()                                
                # fname,lname = name_list.pop(0)," ".join(name_list) if len(name_list) > 2 else name_list[0],name_list[1]
                if len(name_list) > 2:
                    fname,lname = name_list.pop(0)," ".join(name_list)                            
                else:
                    fname,lname = name_list[0],name_list[1]
            except Exception as e:
                fname = "NA"
                lname = "NA"
                            
            try:
                city = html.find(attrs = {'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip('\n')
            except Exception as e:
                city = "NA"

            try:
                designation = html.find(attrs={'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text().strip('\n')
            except Exception as e:
                designation = "NA"


                context.update({
                    LinkdinHeaders.LD_FIRST_NAME:fname,
                    LinkdinHeaders.LD_LAST_NAME:lname,
                    LinkdinHeaders.LD_COMPANY_NAME:company[0],
                    LinkdinHeaders.LD_DESIGNATIONS:designation,
                    LinkdinHeaders.LD_CITIES:city,
                    LinkdinHeaders.LD_URLS:profile_url,
                    LinkdinHeaders.LD_COUNTRIES:""
                })                            
                dict_object.writerow(context) 

    def scrap_linkdin_jobs(self):  
        companies_code = [
            ("aditya-birla-capital","40439053"),
            # ("Aditya Birla Chemicals (Thailand)","28605919"),
        ]        
        # "VP IT","CTO","Director IT","Head IT -(Technology)","VP-IT",
        designations = ["Vice President - IT"]      
          
        with open(self.FILE_NAME, "a") as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=self.HEADERS_LIST)
            dict_object.writeheader()
            
             
            for company in companies_code:                   
                for designation in designations:
                    context = {}

                    url = '''https://www.linkedin.com/search/results/people/?currentCompany=%5B%22{linkdin_company_code}%22%5D&keywords={company_name}&origin=FACETED_SEARCH&title={designation}
                    '''.format(linkdin_company_code = company[1],company_name=company[0],designation=designation.replace(' ','%20') if designation.isspace() else designation)
                        
                    self.driver.get(url)
                    time.sleep(120)

                    soup=BeautifulSoup(self.driver.page_source, 'html.parser')
                    

                    if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                        continue
                        
                    # total_records = int(soup.find(attrs={'class':'pb2 t-black--light t-14'}).get_text().strip('\n').split()[0])    
                    # page = round(total_records/self.TOTAL_RECORDS_ON_SINGLE_PAGE)                      
                    # has_pagination = False
                    

                        
                    # if page > 0 and has_pagination:
                    #     print("....................................IF condition executing.............................")
                    #     print("next pagination..")
                    #     for page_num in range(1,page+1):
                    #         print(page_num,"|||||||||||||||||||||||||||||||||||||||||||||||")
                    #         url = '''https://www.linkedin.com/search/results/people/?currentCompany=%5B%22{linkdin_company_code}%22%5D&keywords={company_name}&origin=FACETED_SEARCH&title={designation}&page={page_num_size}
                    #             '''.format(linkdin_company_code = company[1],company_name=company[0],designation=designation.replace(' ','%20') if designation.isspace() else designation,page_num_size=page_num)
                    #         print(url,"........................URL...................")
                    #         self.driver.get(url)

                    #         if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                    #             continue

                    #         ###################################################################################################################
                    #         for html in soup.find(attrs={'class':'reusable-search__entity-result-list list-style-none'}).findAll(attrs={'class':'reusable-search__result-container'}):                                              
                    #             try:
                    #                 profile_url = html.find(attrs={'class':'app-aware-link scale-down'})['href']
                    #             except Exception as e:
                    #                 profile_url = "NA"

                    #             try:
                    #                 name = html.findAll('span',attrs={'aria-hidden':'true'})[0].get_text()                        
                    #                 name_list = name.split()                                
                    #                 # fname,lname = name_list.pop(0)," ".join(name_list) if len(name_list) > 2 else name_list[0],name_list[1]
                    #                 if len(name_list) > 2:
                    #                     fname,lname = name_list.pop(0)," ".join(name_list)                            
                    #                 else:
                    #                     fname,lname = name_list[0],name_list[1]
                    #             except Exception as e:
                    #                 fname = "NA"
                    #                 lname = "NA"
                                    
                    #             try:
                    #                 city = html.find(attrs = {'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip('\n')
                    #             except Exception as e:
                    #                 city = "NA"

                    #             try:
                    #                 designation = html.find(attrs={'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text().strip('\n')
                    #             except Exception as e:
                    #                 designation = "NA"


                    #             context.update({
                    #                 LinkdinHeaders.LD_FIRST_NAME:fname,
                    #                 LinkdinHeaders.LD_LAST_NAME:lname,
                    #                 LinkdinHeaders.LD_COMPANY_NAME:company[0],
                    #                 LinkdinHeaders.LD_DESIGNATIONS:designation,
                    #                 LinkdinHeaders.LD_CITIES:city,
                    #                 LinkdinHeaders.LD_URLS:profile_url,
                    #                 LinkdinHeaders.LD_COUNTRIES:""
                    #             })                            
                    #             dict_object.writerow(context) 

                            ###################################################################################################################

                    print("........................ELSE CODE EXECUTING...........")
                    for html in soup.find(attrs={'class':'reusable-search__entity-result-list list-style-none'}).findAll(attrs={'class':'reusable-search__result-container'}):                      
                        
                        try:
                            profile_url = html.find(attrs={'class':'app-aware-link scale-down'})['href']
                        except Exception as e:
                            profile_url = "NA"

                        try:
                            name = html.findAll('span',attrs={'aria-hidden':'true'})[0].get_text()                        
                            name_list = name.split()                                
                            # fname,lname = name_list.pop(0)," ".join(name_list) if len(name_list) > 2 else name_list[0],name_list[1]
                            if len(name_list) > 2:
                                fname,lname = name_list.pop(0)," ".join(name_list)                            
                            else:
                                fname,lname = name_list[0],name_list[1]
                        except Exception as e:
                            fname = "NA"
                            lname = "NA"
                            
                        try:
                            city = html.find(attrs = {'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip('\n')
                        except Exception as e:
                            city = "NA"

                        try:
                            designation = html.find(attrs={'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text().strip('\n')
                        except Exception as e:
                            designation = "NA"


                        context.update({
                            LinkdinHeaders.LD_FIRST_NAME:fname,
                            LinkdinHeaders.LD_LAST_NAME:lname,
                            LinkdinHeaders.LD_COMPANY_NAME:company[0],
                            LinkdinHeaders.LD_DESIGNATIONS:designation,
                            LinkdinHeaders.LD_CITIES:city,
                            LinkdinHeaders.LD_URLS:profile_url,
                            LinkdinHeaders.LD_COUNTRIES:""
                        })                            
                        dict_object.writerow(context)
                    # has_pagination = True     
                time.sleep(30)
            time.sleep(30)
        time.sleep(30)
        
 
logging.warning("{0} Program start time...".format(time.time()))
ScrapLinkdinJobs().linkdin_login()
logging.warning("{0} Execution completed...".format(time.time()))
