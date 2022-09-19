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
COMPANIES = [
            ("aditya-birla-capital","40439053"),
            ("Aditya Birla Chemicals (Thailand)","28605919"),
            ("Aditya Birla Fashion and Retail Limited (ABFRL)","164809"),
            # ("Aditya Birla Grasun Chemicals (Fangchenggang) Limited","18105465"),
            # ("Aditya Birla Insulators","29076845"),
            # ("Aditya Birla Science and Technology Company Private Limited (ABSTCPL)","80665870"),
            # ("AV Group NB","24787889"),
            # ("Birla Carbon","6374"),
            # ("Birla Jingwei Fibres Company Limited (BJFCL)","8912518"),
            # ("Dahej Harbour and Infrastructure Limited (DHIL)","27990634"),
            # ("Domsjö Fabriker (Domsjö)","733042"),
            # ("Essel Mining & Industries Limited (EMIL)","13609540"),
            # ("Grasim Industries Limited","9680758"),
            # ("Hindalco Industries Limited","81855"),
            # ("Hindalco-Almex Aerospace Limited (HAAL)","27312462"),            
            # ("PT Elegant Textile Industry (Indonesia)","8588207"),
            # ("PT Indo Bharat Rayon (Indonesia)","9809612"),
            # ("PT Indo Liberty Textiles (Indonesia)","9115535"),            
            # ("PT Sunrise Bumi Textiles (Indonesia)","5414133"),
            # ("Swiss Singapore Overseas Enterprises Pte Ltd (SSOE)","5715503"),
            # ("Tanfac Industries Limited","27601474"),
            # ("Terrace Bay Pulp Mill","8213099"),
            # ("Thai Acrylic Fibre Co. Ltd (TAF)","155568"),
            # ("Thai Peroxide Company Limited (TPL)","33844256"),            
            # ("UltraTech Cement Limited","3810876"),
            # ("Utkal Alumina International Limited","5966378"),
            # ("Vodafone Idea Limited","14439560"),
            # ("Indo Thai Synthetics Company Limited","33858788"),
            # ("Novelis Inc","14822852"),
            # ("Thai Rayon","6513197"),
            # ("Indo Phil Group of Companies",""),
            # ("Indo Phil Textile Mills",""),
            # ("PT Indo Raya Kimia (Indonesia)","")
        ]

# DESIGNATIONS = ("CIO" , "CTO" , "CISO" , "Director IT" , "VP IT" , "Head IT- (Technology)",
#                 "Procurement Director" , "VP" , "Manager" , "Head",
#                 "CHRO" , "HR Manager" , "HR Director" , "VP HR" , "Head HR","Head HR"
#                 )
DESIGNATIONS = ('Manager',)


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
    global var_page
    var_page = 1

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
                  
        with open(self.FILE_NAME, "a") as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=self.HEADERS_LIST)
            dict_object.writeheader()
             
            for company in COMPANIES:       
                for designation in DESIGNATIONS:
                    context = {}

                    url = '''https://www.linkedin.com/search/results/people/?currentCompany=%5B%22{linkdin_company_code}%22%5D&keywords={company_name}&origin=FACETED_SEARCH&title={designation}
                    '''.format(linkdin_company_code = company[1],company_name=company[0],designation=designation.replace(' ','%20') if designation.isspace() else designation)
                        
                    self.driver.get(url)
                    time.sleep(60)

                    soup=BeautifulSoup(self.driver.page_source, 'html.parser')
                    

                    if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                        continue

                    
                    
                    li = []
                    for val in soup.find(attrs={'class':'pb2 t-black--light t-14'}).get_text().strip('\n').split():
                        if ',' in val:
                            val = val.replace(',','')

                        try:
                            val = int(val)
                        except Exception as e:
                            val = None

                        if val:
                            li.append(val)
                    total_records = li[0]
                    page = round(total_records/self.TOTAL_RECORDS_ON_SINGLE_PAGE)                      
                    
                    var_page = page
                    for page_num in range(1,var_page+1):
                        print(page_num,">>>")
                        

                        if page_num == 1:
                            url = url
                        else:
                            
                            url = url + '&page={page_number}'.format(page_number=page_num)
                        
                        self.driver.get(url)
                        soup=BeautifulSoup(self.driver.page_source, 'html.parser')
                    

                        if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                            continue

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
                                designation = html.find(attrs={'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text().strip('\n')
                            except Exception as e:
                                designation = "NA"

                            try:
                                city = html.find(attrs = {'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip('\n')
                            except Exception as e:
                                city = "NA"

                            
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
                            time.sleep(10)
                            print("-----------------------------------------------------")                    
                       
                time.sleep(10)
            time.sleep(10)
        time.sleep(10)
        
 
logging.warning("{0} Program start time...".format(time.time()))
ScrapLinkdinJobs().linkdin_login()
logging.warning("{0} Execution completed...".format(time.time()))
