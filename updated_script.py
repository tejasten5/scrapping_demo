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




salary=[]
experience=[]
Location=[]
description=[]
role=[]
industry_type=[]
qualification=[]
Functional_area=[]
Employment_type=[]
Role_category=[]
about_company=[]
skills=[]
designation = []

# designation = []


# Designation



# Job_description
# Education
# Address
# Post_by
# Post date
# designation
# Website
# url

for lin in range(len(Link)):
    driver.get(Link[lin])
    #time.sleep(1)
    soup=BeautifulSoup(driver.page_source, 'lxml') 
    
    


    if soup.find(attrs={'class':"salary"})==None: #to skip the error
        continue
    else:

        experience.append(soup.find(attrs={'class':"exp"}).text)
        salary.append(soup.find(attrs={'class':"salary"}).text)
        Location.append(soup.find(attrs={'class':'loc'}).find('a').text)
        designation.append(soup.find(attrs={'class':"jd-header-title"}).text)
        
        description.append(soup.find(attrs={'class':"job-desc"}).text)
            

        details=[]

        for i in soup.find(attrs={'class':"other-details"}).findAll(attrs={'class':"details"}):
            details.append(i.text)
        
        role.append(details[0])
        industry_type.append(details[1])

        Functional_area.append(details[2])
        Employment_type.append(details[3])
        Role_category.append(details[4])

        qual=[]
        for i in soup.find(attrs={'class':"education"}).findAll(attrs={'class':'details'}):
            qual.append(i.text)
        qualification.append(qual)
        sk=[]
        for i in soup.find(attrs={'class':"key-skill"}).findAll('a'):
            sk.append(i.text)
        skills.append(sk)

        about_company.append(soup.find(attrs={'class':"about-company"}).find(attrs={'class':"detail dang-inner-html"}).text)





df=pd.DataFrame()
df['designation'] = designation
df['salary']=salary
df['experience']=experience
df['Location']=Location
df['role']=role
df['description']=description
df['skills']=skills
df['qualification']=qualification
df['industry_type']=industry_type
df['Functional_area']=Functional_area
df['Employment_type']=Employment_type
df['Role_category']=Role_category
df['about_company']=about_company


df.to_csv('naukri.csv',index=False)
