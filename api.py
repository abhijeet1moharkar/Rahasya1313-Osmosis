from eve import Eve
from flask import render_template, request, redirect, url_for, session, escape, Response, jsonify, send_file
from eve.auth import BasicAuth
from eve.methods.get import get_internal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug import secure_filename
from bson import regex

import zipfile
import json
import pathlib
import hashlib
import requests
import random
import os
from datetime import datetime
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
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

port = 5000
#host = '142.93.209.128'
host = "0.0.0.0"


class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == 'rahasya' and password == '1313'


app = Eve(__name__, auth=MyBasicAuth)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '5234124584324'

headers = {'Authorization': 'Basic aGVsbG86Z29h==',
           'Content-Type': 'application/json'}

app.config['MONGO_HOST'] = '0.0.0.0'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'hackit'
app.config['MONGO_USERNAME'] = 'rahasya'
app.config['MONGO_PASSWORD'] = '1313'

UPLOAD_FOLDER = "./static/uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
client = app.data.driver.db.client
db = client['hackit']

@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload_single', methods=['GET', 'POST'])
def upload_doc():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['resume']
        # if user does not select file, browser also
        # submit a empty part without filename
        print('Entered')
        print(file.filename)
        if file:
            print('andar hu')
            # filename = secure_filename(file.filename)
            file.save(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = ResumeParser(file.filename).get_extracted_data()
            data["f_loc"] = file.filename 
            #
            db.resume.insert_one(data)
            return redirect('/index')


@app.route('/upload_zip', methods=['GET', 'POST'])
def upload_zip():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['resume']
        # if user does not select file, browser also
        # submit a empty part without filename
        print('Entered')
        print(file.filename)
        if file:
            print('andar hu')
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print('.\n'*50, filename)
            with zipfile.ZipFile(file.filename, 'r') as zip_ref:
                zip_ref.extractall('zip/')
            return redirect('/index')


def scrap(s, linked):
    soup = BeautifulSoup(s, "html.parser")

    experiance = []
    education = {}
    patents = []
    score = []
    skills = []

    for row in soup.findAll('li', attrs={'class': 'result-card experience-item'}):
        experiance.append(str(row.h3.text)+" at "+str(row.h4.text))
    name = soup.find('ul', attrs={'class': 'pv-top-card--list'}
                     ).find('li', attrs={'class': 'break-words'}).text
    for i in soup.find('section', attrs={'class': 'education-section'}).find('ul', attrs={'class': 'pv-profile-section__section-info'}).findAll('li', attrs={'class': 'pv-education-entity'}):
        try:
            education['college'] = i.h3.text
            education['rest'] = i.p.text
        except:
            education['college'] = i.h3.text

    for i in soup.findAll('span', attrs={'class': 'pv-skill-category-entity__name-text'}):
        tmp = i.text.split('\n')
        tmp = ' '.join(tmp)
        tmp = tmp.replace(' ', '')
        skills.append(tmp)
    skills = ' '.join(map(str, skills))

    return [name, linked, skills]


@app.route('/linkedinsearch', methods=['GET', 'POST'])
def linkedinsearch():
    if request.method == 'POST':
        # check if the post request has the file part
        keyword = request.form['searchkey']
        options = Options()
        options.headless=True
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
        driver.find_element_by_id("username").send_keys('atharva.gondkar@gmail.com')
        driver.find_element_by_id("password").send_keys('amway2775035')
        driver.find_element_by_xpath("/html/body/div/main/div/form/div[3]/button").click()
        #, 'Manager', 'Web Developer', 'React Developer','Java Developer', 'IOS Developer'
  
        tmpd={}
        d = pd.DataFrame(columns=['name','linkedin','skills'])
       
        driver.get('https://www.linkedin.com/search/results/people/?keywords='+keyword+'&origin=SUGGESTION')
        #driver.find_element_by_xpath("/html/body/header/div/form/div/div/div/div/div[1]/div/input").send_keys(i+Keys.ENTER)
        content=driver.find_element_by_class_name('blended-srp-results-js')
        source_code = content.get_attribute("innerHTML")
        soup = BeautifulSoup(source_code, "html.parser")

        

        data = soup.findAll('a',{'class':'search-result__result-link'})
        count=0
        for j in data :
            if count%2==0:
                pass
            driver.get("https://www.linkedin.com"+str(j['href']))
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                element = driver.find_element_by_class_name('pv-skill-categories-section')
                actions = ActionChains(driver)
                actions.move_to_element(element).click()
            except:
                element = driver.find_element_by_class_name('pv-profile-section__card-heading')
                actions = ActionChains(driver)
                actions.move_to_element(element).click()
            finally:
                driver.execute_script("arguments[0].scrollIntoView();", element)
                myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pv-profile-section__card-action-bar')))
            

        
            
            #driver.find_element_by_class_name('pv-skill-categories-section').click()
            content=driver.find_element_by_class_name('core-rail')
            print(str(content))
            tmp=scrap(content.get_attribute("innerHTML"),j['href'])
            d.loc[len(d)] = tmp

            main=[]
            main = content.get_attribute("innerHTML")
            #print(main)
            

    #directory='C:\\Users\\atharva\\.spyder-py3\\'

    d.to_csv('d.csv')#, delimiter=None, index_col=0)


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
    # fetch('http://142.93.209.128:5000/places?where={"$or":[{"Cat": {"$regex":"'+search+'","$options" : "i"}},{"BusinessName": {"$regex":"'+search+'","$options" : "i"}}]}', {
