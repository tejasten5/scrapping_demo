# from selenium import webdriver
# from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
import pandas as pd
import os,csv,time,logging
# from dotenv import load_dotenv
# load_dotenv()
 
# # USER_EMAIL 
# # USER_PASSWORD 

# COMPANY_NAMES = [
#     'Aditya Birla Capital Limited',
#     'Vodafone Idea Limited',
#     'Aditya Birla Chemicals (Thailand)',
#     'Aditya Birla Grasun Chemicals (Fangchenggang)',
#     # 'Aditya Birla Fashion and Retail Limited',
#     # 'Aditya Birla Insulators',
#     # 'Aditya Birla Science and Technology Company Private Limited',
#     # 'AV Group NB',
#     # 'Birla Carbon',
#     # 'Birla Jingwei Fibres Company Limited',
#     # 'Dahej Harbour and Infrastructure Limited',
#     # 'Domsjö Fabriker',
#     # 'Essel Mining & Industries Limited',
#     # 'Grasim Industries Limited',
#     # 'Hindalco Industries Limited',
#     # 'Hindalco-Almex Aerospace Limited',
#     # 'Indo Phil Group of Companies',
#     # 'Indo Phil Textile Mills',
#     # 'Indo Thai Synthetics Company Limited',
#     # 'Novelis Inc',
#     # 'PT Elegant Textile Industry (Indonesia)',
#     # 'PT Indo Bharat Rayon (Indonesia)',
#     # 'PT Indo Liberty Textiles (Indonesia)',
#     # 'PT Indo Raya Kimia (Indonesia)',
#     # 'PT Sunrise Bumi Textiles (Indonesia)',
#     # 'Swiss Singapore Overseas Enterprises Pte Ltd',
#     # 'Tanfac Industries Limited',
#     # 'Terrace Bay Pulp Mill',
#     # 'Thai Acrylic Fibre Co. Ltd',
#     # 'Thai Peroxide Company Limited',
#     # 'Thai Rayon',
#     # 'UltraTech Cement Limited',
#     # 'Utkal Alumina International Limited'    
# ]

# DESIGNATION = [
#     # 'CIO', 'CTO', 'CISO','Director IT', 'VP IT','Head IT- (Technology)',
#     # 'Procurement Director', 'VP','Manager','Head','CHRO'
#     'HR Manager','HR Director','VP HR','Head HR',
# ]

# class LinkdinHeaders:
#     LD_DESIGNATION = 'Designation'    
#     LD_NAME = 'Name'

# class ScrapLinkdinProfiles:
#     LINKDIN_LOGIN_URL = "https://www.linkedin.com/login"
#     FILE_NAME = "linkdin_profiles.csv"    
#     LINKDIN_PROFILE_SEARCH_URL = 'https://www.linkedin.com/search/results/people/?company={company_name}&sid=Rd7&title={designation}'

#     def __init__(self,area_of_search=None):
#         options = webdriver.ChromeOptions()
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--incognito')
#         options.add_argument('--headless')
#         self.driver = webdriver.Chrome(ChromeDriverManager().install())    

#     def linkdin_login(self): 
        
#         self.driver.get(self.LINKDIN_LOGIN_URL)
#         time.sleep(5)

#         soup=BeautifulSoup(self.driver.page_source, 'lxml')
#         username     = self.driver.find_element(By.ID,"username")
#         username.send_keys(os.environ.get('USER_EMAIL'))

#         pword = self.driver.find_element(By.ID,"password")
#         pword.send_keys(os.environ.get('USER_PASSWORD'))		
#         self.driver.find_element(By.XPATH,"//button[@type='submit']").click()
#         time.sleep(3)

#         self.scrap_profile_data()

#         time.sleep(5)
#         self.driver.close()

#     def url_generator(self, url_list):
#         for url in url_list:
#             yield url

#     def scrap_profile_data(self):           
#         url_list = [self.LINKDIN_PROFILE_SEARCH_URL.format(company_name=company_name,designation = designation) for company_name in COMPANY_NAMES for designation in DESIGNATION]
        
#         with open(self.FILE_NAME, 'a',encoding="utf-8") as csv_file:
#             dict_object = csv.DictWriter(csv_file, fieldnames=[LinkdinHeaders.LD_DESIGNATION, LinkdinHeaders.LD_NAME])
#             dict_object.writeheader()
            

#             for url in self.url_generator(url_list):
#                 time.sleep(5)                
#                 self.driver.get(url)
#                 context = {}
                
#                 soup=BeautifulSoup(self.driver.page_source, 'lxml')
                

#                 if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
#                     continue
#                 else:
#                     try:
#                         full_name = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]').text
#                     except Exception as e:
#                         full_name = "NA"

#                     try:
#                         designation = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[2]/div/div[1]').text
#                     except Exception as e:
#                         designation = "NA"    

#                     print(designation,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>",full_name)

#                     context.update({LinkdinHeaders.LD_DESIGNATION:designation,LinkdinHeaders.LD_NAME:full_name})
#                     print(context,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#                 dict_object.writerow(context)
#                 time.sleep(10)          
        

# logging.warning("{0} Program start time...".format(time.time()))
# area_of_search = "php"
# ScrapLinkdinProfiles(area_of_search).linkdin_login()
# logging.warning("{0} Execution completed...".format(time.time()))


read_CSV = pd.read_csv('E:\scrapping\scrapping_project\scrapping_demo\linked_profile.csv')

filtered_df = read_CSV[read_CSV['Desigation'].str.contains('VP')]
filtered_df.to_csv('output.csv')