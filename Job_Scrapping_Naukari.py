from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



class ScrapNaukriJobs:
    BASE_URL = 'https://www.naukri.com/'
    FILE_NAME = 'scrap_naukri_jobs.csv'

    CTC_FILTER_QUERY_PARAMS = '&ctcFilter=101&ctcFilter=15to25&ctcFilter=25to50&ctcFilter=50to75&ctcFilter=75to100'
    CITY_FILTER_PARAMS = '&cityTypeGid=6&cityTypeGid=17&cityTypeGid=73&cityTypeGid=97&cityTypeGid=134&cityTypeGid=139&cityTypeGid=183&cityTypeGid=220&cityTypeGid=232&cityTypeGid=9508&cityTypeGid=9509'

    def __init__(self,language):
        print("...Initializing....")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.language = language.lower()
        self.job_detail_links = []

    def get_job_detail_links(self):
        print("Getting job detail links....")
        for page in range(1,11):
            query_param = f'{self.language}-jobs' 

            URL = f"{self.BASE_URL}{query_param}?k={self.language}{self.CTC_FILTER_QUERY_PARAMS}{self.CITY_FILTER_PARAMS}" page == 1 else f"{self.BASE_URL}{query_param}-{str(page)}?k={self.language}{self.CTC_FILTER_QUERY_PARAMS}{self.CITY_FILTER_PARAMS}"
            
            self.driver.get(URL)
            timeDelay = random.randrange(0, 5)
            time.sleep(timeDelay) 
            soup=BeautifulSoup(self.driver.page_source, 'lxml')

            for i in soup.findAll(attrs={'class':"jobTuple bgWhite br4 mb-8"}):
                for j in i.findAll(attrs={'class':"title fw500 ellipsis"}):
                    self.job_detail_links.append(j.get('href'))
            
    def scrap_details(self):
        print("Scraping call started...")
        self.get_job_detail_links()
        time.sleep(2)
        designation_list,company_name_list,experience_list,salary_list = [],[],[],[]        
        location_list,job_description_list,role_list,industry_type_list = [],[],[],[]        
        functional_area_list,employment_type_list,role_category_list,education_list = [],[],[],[]       
        key_skill_list,about_company_list,address_list,post_by_list = [],[],[],[]       
        post_date_list,website_list,url_list = [],[],[]

        print(len(self.job_detail_links),"??????????????????????????????????")

        for link in range(len(self.job_detail_links)):
            print(self.job_detail_links[link],">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",link)

            self.driver.get(self.job_detail_links[link])    
            soup=BeautifulSoup(self.driver.page_source, 'lxml')

            if soup.find(attrs={'class':"salary"})==None: 
                continue
            else:
                company_name_list.append(soup.find(attrs={'class':"jd-header-comp-name"}).text)
                experience_list.append(soup.find(attrs={'class':"exp"}).text)
                salary_list.append(soup.find(attrs={'class':"salary"}).text)
                location_list.append(soup.find(attrs={'class':'loc'}).find('a').text)
                designation_list.append(soup.find(attrs={'class':"jd-header-title"}).text)                
                job_description_list.append(soup.find(attrs={'class':"job-desc"}).text)               
                post_date_list.append([i for i in soup.find(attrs={'class':"jd-stats"})][0].text.split(':')[1])
                website_list.append(soup.find(attrs={'class':"jd-header-comp-name"}).contents[0])
                url_list.append(soup.find(attrs={'class':"jd-header-comp-name"}).contents[0])                

                details=[]
                for i in soup.find(attrs={'class':"other-details"}).findAll(attrs={'class':"details"}):
                    details.append(i.text)

                role_list.append(details[0])
                industry_type_list.append(details[1])
                functional_area_list.append(details[2])
                employment_type_list.append(details[3])
                role_category_list.append(details[4])

                qual=[]
                for i in soup.find(attrs={'class':"education"}).findAll(attrs={'class':'details'}):
                    qual.append(i.text)
                education_list.append(qual)

                sk=[]
                for i in soup.find(attrs={'class':"key-skill"}).findAll('a'):
                    sk.append(i.text)
                key_skill_list.append(",".join(sk))                

                if soup.find(attrs={'class':"name-designation"})==None:
                    post_by_list.append("NA")
                else:
                    post_by_list.append(soup.find(attrs={'class':"name-designation"}).text)


                if soup.find(attrs={'class':"about-company"})==None:                    
                    about_company_list.append("NA")                    
                else:
                    
                    address_list.append("NA" if soup.find(attrs={'class':"about-company"}).find(attrs={'class':"comp-info-detail"}) == None else soup.find(attrs={'class':"about-company"}).find(attrs={'class':"comp-info-detail"}).text)  

                    about_company_list.append(soup.find(attrs={'class':"about-company"}).find(attrs={'class':"detail dang-inner-html"}).text)

                



        df=pd.DataFrame()
        df['Designation'] = designation_list
        df['Company Name'] = company_name_list
        df['Salary']=salary_list
        df['Experience']=experience_list
        df['Location']=location_list
        df['Role']=role_list
        df['Skills']=key_skill_list
        df['Qualification']=education_list
        df['Industry Type']=industry_type_list
        df['Functional Area']=functional_area_list
        df['Employment Type']=employment_type_list
        df['Role Category']=role_category_list
        df['Address'] = address_list
        df['Post By'] = post_by_list
        df['Post Date'] = post_date_list
        df['Website'] = website_list
        df['Url'] = url_list
        df['Job Description']=job_description_list
        df['About Company']=about_company_list

        df.to_csv(self.FILE_NAME,index=False)
        self.driver.close()
        

print("Program star time...",time.time())
scrap_naukri = ScrapNaukriJobs("PYTHON")
scrap_naukri.scrap_details()
print("Execution completed...",time.time())
