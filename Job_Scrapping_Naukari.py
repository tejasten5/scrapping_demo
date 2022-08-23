import time,csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class XPATHConstant:
    DELAY = 20 
    BASE_URL = 'https://www.naukri.com/'

    #CSV file data
    FILE_NAME = 'Naukri_scrape.csv'
    FILE_MODE = 'a'
    CSV_HEADERS = ['Designation', 'Company name', 'URL', 'Experience', 'Salary','Description','Job Description']
    
    # Filters 
    CTC_FILTER_QUERY_PARAMS = '&ctcFilter=101&ctcFilter=15to25&ctcFilter=25to50&ctcFilter=50to75&ctcFilter=75to100'
    CITY_FILTER_PARAMS = '&cityTypeGid=6&cityTypeGid=17&cityTypeGid=73&cityTypeGid=97&cityTypeGid=134&cityTypeGid=139&cityTypeGid=183&cityTypeGid=220&cityTypeGid=232&cityTypeGid=9508&cityTypeGid=9509'
    
    # Xpath
    HREF_XPATH = '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[1]/div[1]/div[1]/a'
    DESIGNATION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[1]/div[1]/div[1]/header/h1'
    COMPANY_NAME_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[1]/div[1]/div[1]/div/a[1]'
    EXPERIENCE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[1]/span'
    LOCATION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[3]/span/span'
    SALARY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[2]/span'
    JOB_DESCRIPTION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[1]/p[2]'
    ROLE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[1]/span'
    INDUSTRY_TYPE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[2]/span'
    FUNCTIONAL_AREA_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[3]/span'
    EMPLOYMENT_TYPE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[4]/span'
    ROLE_CATEGORY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[2]/div[1]/span'
    EDUCATION_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[3]'
    KEY_SKILL_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[2]/div[4]'
    ABOUT_COMPANY_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[3]/div[1]'
    ADDRESS_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[3]/div[3]/span'	
    POST_BY_XPATH = ''
    POST_DATE_XPATH = '//*[@id="root"]/main/div[2]/div[2]/section[1]/div[2]/div[1]/span[1]/span'
    WEBSITE_XPATH = ''	
    URL_XPATH = ''

    XPATH_LIST = [
        DESIGNATION_XPATH,
        COMPANY_NAME_XPATH,
        EXPERIENCE_XPATH,
        LOCATION_XPATH,
        SALARY_XPATH,
        JOB_DESCRIPTION_XPATH,
        ROLE_XPATH,
        INDUSTRY_TYPE_XPATH,
        FUNCTIONAL_AREA_XPATH,
        EMPLOYMENT_TYPE_XPATH,
        ROLE_CATEGORY_XPATH,
        EDUCATION_XPATH,
        KEY_SKILL_XPATH,
        ABOUT_COMPANY_XPATH,
        ADDRESS_XPATH,
        # POST_BY_XPATH,
        POST_DATE_XPATH,
        WEBSITE_XPATH,
        URL_XPATH
    ]



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
        self.find_links()
        time.sleep(20)
        self.driver.close()

    def find_links(self):                
        links = self.driver.find_elements(By.XPATH,self.HREF_XPATH)

        for link in links:    
            window_url = link.get_attribute('href')            
            self.driver.execute_script("window.open('%s', '_blank')" % window_url)
            self.driver.switch_to.window(self.driver.window_handles[-1])          
            self.capture_data(link)      
            time.sleep(5)

    def capture_data(self,link):
        for data in self.XPATH_LIST:
            try:
                designation = self.wait.until(EC.presence_of_element_located((By.XPATH,data))).text
            except Exception as e:                
                designation = "NULL"
            
            print(designation,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    def generate_csv(self):
        pass
        
       
scrap_jobs = ScrapLinkdinJob("java")
scrap_jobs.open_browser()

