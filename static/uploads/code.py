from selenium import webdriver
import datetime
import time
import argparse
import os
import getpass
from bs4 import BeautifulSoup 
import urllib
import csv
import re
import os.path
import urllib3
import smtplib
import parser

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#options = Options()
#options.headless=True
def scrap(s):
    soup = BeautifulSoup(s, "html.parser")
    experiance = []
    education={}
    patents=[]
    score=[]
    skills=[]
    for row in soup.findAll('li', attrs = {'class':'result-card experience-item'}):
        experiance.append(str(row.h3.text)+" at "+str(row.h4.text))

    for i in soup.find('section', attrs = {'class':'education-section'}).find('ul', attrs = {'class':'pv-profile-section__section-info'}).findAll('li', attrs = {'class':'pv-education-entity'}):
        education['college']=i.h3.text
        education['rest']=i.p.text

    for i in soup.findAll('span',attrs={'class':'pv-skill-category-entity__name-text'}):
    	tmp=i.text.split('\n')
        tmp=' '.join(tmp)
        tmp=tmp.replace(' ','')
        skills.append(tmp)
  
    '''data=[[soup.find('ul', attrs = {'class':'pv-top-card--list '}).find('li':attrs={'class':'inline'}).text,
           soup.find('span', attrs = {'class':'top-card__subline-item'}).text,
           str(experiance).replace("'",'').replace('[','').replace(']',''),
           str(education).replace("'",'').replace('[','').replace(']',''),
           str(patents).replace("'",'').replace('[','').replace(']',''),
           str(score).replace("'",'').replace('[','').replace(']','')
           ]]
    df=pd.DataFrame(data,columns=['name','profession','loc','experiance','edu','patents','score'])
'''
    print(skills)


parser = argparse.ArgumentParser()
parser.add_argument('-url', '--url', help='URL to the online repository of images')
args = vars(parser.parse_args())
url = args['url']
url = "https://www.linkedin.com/login"

#userid = str(input("Enter email address or number with country code: "))
#password = getpass.getpass('Enter your password:')
# Initialize the Chrome webdriver and open the URL
firefoxProfile = FirefoxProfile()

## Disable images
firefoxProfile.set_preference('permissions.default.image', 2)

driver = webdriver.Firefox(firefoxProfile)
driver.get(url)
driver.implicitly_wait(3)
driver.find_element_by_id("username").send_keys('ramsuthar305@gmail.com')
driver.find_element_by_id("password").send_keys('8149379515r')
driver.find_element_by_xpath("/html/body/div/main/div/form/div[3]/button").click()

driver.find_element_by_xpath("/html/body/header/div/form/div/div/div/div/div[1]/div/input").send_keys('OOP'+Keys.ENTER)
content=driver.find_element_by_class_name('blended-srp-results-js')
source_code = content.get_attribute("innerHTML")
soup = BeautifulSoup(source_code, "html.parser")



data = soup.findAll('a',{'class':'search-result__result-link'})
for i in data :
	driver.get("https://www.linkedin.com"+str(i['href']))
	myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pv-profile-section__card-action-bar')))
	driver.find_element_by_class_name('pv-profile-section__card-action-bar').click()
	content=driver.find_element_by_class_name('core-rail')
	print(str(content))
	scrap(content.get_attribute("innerHTML"))
	main=[]
	main = content.get_attribute("innerHTML")
	#print(main)
