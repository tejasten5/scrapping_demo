from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(ChromeDriverManager().install())


Link=[]
for page in range(1,3): #first 50 pages of the naukri search   

    url = "https://www.naukri.com/python-jobs?k=python" if page == 1 else f"https://www.naukri.com/python-jobs-{str(page)}?k=python"

    driver.get(url)
    timeDelay = random.randrange(0, 5)
    time.sleep(timeDelay) 
    soup=BeautifulSoup(driver.page_source, 'lxml')#returns html of the page

    for i in soup.findAll(attrs={'class':"jobTuple bgWhite br4 mb-8"}):
        for j in i.findAll(attrs={'class':"title fw500 ellipsis"}):
            Link.append(j.get('href')) #stores all the link of the job postings


designation_list = []
company_name_list = []
experience_list = []
salary_list = []
location_list = []
job_description_list = []
role_list = []
industry_type_list = []
functional_area_list = []
employment_type_list = []
role_category_list = []
education_list = []
key_skill_list = []
about_company_list = []
address_list = []
post_by_list = []
post_date_list = []
website_list = []
url_list = []


for lin in range(len(Link)):
    driver.get(Link[lin])    
    soup=BeautifulSoup(driver.page_source, 'lxml')   


    if soup.find(attrs={'class':"salary"})==None: #to skip the error
        continue
    else:

        company_name_list.append(soup.find(attrs={'class':"jd-header-comp-name"}).text)

        experience_list.append(soup.find(attrs={'class':"exp"}).text)
        salary_list.append(soup.find(attrs={'class':"salary"}).text)
        location_list.append(soup.find(attrs={'class':'loc'}).find('a').text)
        designation_list.append(soup.find(attrs={'class':"jd-header-title"}).text)
        
        job_description_list.append(soup.find(attrs={'class':"job-desc"}).text)
        

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

        about_company_list.append(soup.find(attrs={'class':"about-company"}).find(attrs={'class':"detail dang-inner-html"}).text)
        address_list.append(soup.find(attrs={'class':"about-company"}).find(attrs={'class':"comp-info-detail"}).text)

        if soup.find(attrs={'class':"name-designation"})==None:
            post_by_list.append("NA")
        else:
            post_by_list.append(soup.find(attrs={'class':"name-designation"}).text)
        
        # jd-stats
        post_date_list.append([i for i in soup.find(attrs={'class':"jd-stats"})][0].text.split(':')[1])
        # 
        website_list.append(soup.find(attrs={'class':"jd-header-comp-name"}).contents[0])
        url_list.append(soup.find(attrs={'class':"jd-header-comp-name"}).contents[0])






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


df.to_csv('naukri.csv',index=False)
