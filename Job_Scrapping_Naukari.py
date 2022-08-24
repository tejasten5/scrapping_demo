import time,csv,pandas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class XPATHConstant:
    DELAY = 20 
    NAUKRI_PAGINATION_LIMIT = 20
    BASE_URL = 'https://www.naukri.com/'

    #CSV file data
    FILE_NAME = 'Naukri_scrape.csv'
    FILE_MODE = 'a'
    CSV_HEADERS = ['Designation', 'Company name', 'URL', 'Experience', 'Salary','Description','Job Description']
    
    # Filters 
    CTC_FILTER_QUERY_PARAMS = '&ctcFilter=101&ctcFilter=15to25&ctcFilter=25to50&ctcFilter=50to75&ctcFilter=75to100'
    CITY_FILTER_PARAMS = '&cityTypeGid=6&cityTypeGid=17&cityTypeGid=73&cityTypeGid=97&cityTypeGid=134&cityTypeGid=139&cityTypeGid=183&cityTypeGid=220&cityTypeGid=232&cityTypeGid=9508&cityTypeGid=9509'
    
    # Xpath
    HREF_XPATH = '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[4]/div[1]/div[1]/a'

    DESIGNATION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]/div[1]/header/h1'
    COMPANY_NAME_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]/div[1]/div/a[1]'
    EXPERIENCE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]/div[2]/div[1]/span'
    LOCATION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]/div[2]/div[3]/span/a[1]'
    SALARY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]/div[2]/div[2]/span'
    JOB_DESCRIPTION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]/ul'
    ROLE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[2]/div[1]/span'
    INDUSTRY_TYPE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[2]/div[2]/span'
    FUNCTIONAL_AREA_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[2]/div[3]/span'
    EMPLOYMENT_TYPE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[2]/div[4]/span/span'
    ROLE_CATEGORY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[2]/div[1]/span'
    EDUCATION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[3]'
    KEY_SKILL_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[4]'
    ABOUT_COMPANY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[1]'
    ADDRESS_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[3]/span'	
    POST_BY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/header/div[1]'
    POST_DATE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[{index}]/div[2]/div[1]/span[1]/span'
    WEBSITE_XPATH = ''	
    URL_XPATH = ''

class ScrapLinkdinJob(XPATHConstant):
    def __init__(self, language):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, self.DELAY)
        self.driver.implicitly_wait(10)
        self.language = language.lower()   
            
    
    def open_browser(self):
        query_param = f'{self.language}-jobs'        
        URL = f"{self.BASE_URL}{query_param}?k={self.language}{self.CTC_FILTER_QUERY_PARAMS}{self.CITY_FILTER_PARAMS}"
        self.driver.get(URL)  
        self.record_count = 3        

        link_generator = [f'//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[{idx}]/div[1]/div[1]/a' for idx in range(1,self.record_count)]      
        
        for idx,links in enumerate(link_generator,start=1):                              
            df = self.find_links(links,idx)      
        time.sleep(2)
        self.generate_csv(df)
        self.driver.close()

    def find_links(self,links,idx,df_list=[]):
        new_links = self.driver.find_elements(By.XPATH,links)       
        
        for link in new_links:               
            window_url = link.get_attribute('href')  
            kwargs = self.capture_data(link,idx)     
        df_list.append(kwargs)
        return df_list  
        
        

    def capture_data(self,link,idx):   
        print("...Capturing data...")    
        try:
            designation = self.wait.until(EC.presence_of_element_located((By.XPATH,self.DESIGNATION_XPATH.format(index = idx)))).text
        except Exception as e:     
            designation = "NULL"
        
        try:
            company_name = self.wait.until(EC.presence_of_element_located((By.XPATH,self.COMPANY_NAME_XPATH.format(index = idx)))).text
        except Exception as e:                
            company_name = "NULL"

        try:
            experience = self.wait.until(EC.presence_of_element_located((By.XPATH,self.EXPERIENCE_XPATH.format(index = idx)))).text
        except Exception as e:                
            experience = "NULL"

        try:
            location = self.wait.until(EC.presence_of_element_located((By.XPATH,self.LOCATION_XPATH.format(index = idx)))).text
        except Exception as e:                
            location = "NULL"

        try:
            salary = self.wait.until(EC.presence_of_element_located((By.XPATH,self.SALARY_XPATH.format(index = idx)))).text
        except Exception as e:                
            salary = "NULL"

        try:
            job_description = self.wait.until(EC.presence_of_element_located((By.XPATH,self.JOB_DESCRIPTION_XPATH.format(index = idx)))).text
        except Exception as e:                
            job_description = "NULL"

        try:
            role = self.wait.until(EC.presence_of_element_located((By.XPATH,self.ROLE_XPATH.format(index = idx)))).text
        except Exception as e:                
            role = "NULL"

        try:
            industry_type = self.wait.until(EC.presence_of_element_located((By.XPATH,self.INDUSTRY_TYPE_XPATH.format(index = idx)))).text
        except Exception as e:                
            industry_type = "NULL"

        try:
            functional_area = self.wait.until(EC.presence_of_element_located((By.XPATH,self.FUNCTIONAL_AREA_XPATH.format(index = idx)))).text
        except Exception as e:                
            functional_area = "NULL"

        try:
            employment_type = self.wait.until(EC.presence_of_element_located((By.XPATH,self.EMPLOYMENT_TYPE_XPATH.format(index = idx)))).text
            if ',' in employment_type:
                employment_type  = employment_type.replace(',', ' ')
        except Exception as e:                
            employment_type = "NULL"

        try:
            role_category = self.wait.until(EC.presence_of_element_located((By.XPATH,self.ROLE_CATEGORY_XPATH.format(index = idx)))).text
        except Exception as e:                
            role_category = "NULL"
        
        try:
            education = self.wait.until(EC.presence_of_element_located((By.XPATH,self.EDUCATION_XPATH.format(index = idx)))).text
        except Exception as e:                
            education = "NULL"
        
        try:
            key_skill = self.wait.until(EC.presence_of_element_located((By.XPATH,self.KEY_SKILL_XPATH.format(index = idx)))).text
        except Exception as e:                
            key_skill = "NULL"

        try:
            about_company = self.wait.until(EC.presence_of_element_located((By.XPATH,self.ABOUT_COMPANY_XPATH.format(index = idx)))).text
            if ',' in about_company:
                about_company  = about_company.replace(',', ' ')
        except Exception as e:                
            about_company = "NULL"
        
        try:
            address = self.wait.until(EC.presence_of_element_located((By.XPATH,self.ADDRESS_XPATH.format(index = idx)))).text
            
            if ',' in address:
                address  = address.replace(',', ' ')
        except Exception as e:                
            address = "NULL"

        try:
            post_by = self.wait.until(EC.presence_of_element_located((By.XPATH,self.POST_BY_XPATH.format(index = idx)))).text
        except Exception as e:                
            post_by = "NULL"
        
        try:
            post_date = self.wait.until(EC.presence_of_element_located((By.XPATH,self.POST_DATE_XPATH.format(index = idx)))).text
        except Exception as e:                
            post_date = "NULL"

        try:
            website = self.wait.until(EC.presence_of_element_located((By.XPATH,self.WEBSITE_XPATH.format(index = idx)))).text
        except Exception as e:                
            website = "NULL"

        try:
            website_url = self.wait.until(EC.presence_of_element_located((By.XPATH,self.URL_XPATH.format(index = idx)))).text
        except Exception as e:                
            website_url = "NULL"
        


        kwargs = {
            'designation':designation,
            'company_name':company_name,
            'experience':experience,
            'location':location,
            'salary':salary,
            'job_description':job_description,
            'role':role,
            'industry_type':industry_type,
            'functional_area':functional_area,
            'employment_type':employment_type,
            'role_category':role_category,
            'education':education,
            'key_skill':key_skill,
            'about_company':about_company,
            'address':address,
            'post_by':post_by,
            'post_date':post_date,
            'website':website,
            'website_url':website_url
        }

        print("...return kwargs...")

        return kwargs 

    def generate_csv(self,df_list):
        print(df_list,">>>>>")
        df = pandas.DataFrame(df_list)
        df.to_csv(self.FILE_NAME, sep='\t', encoding='utf-8')

       
scrap_jobs = ScrapLinkdinJob("java")
scrap_jobs.open_browser()

