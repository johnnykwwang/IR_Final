from pymongo import MongoClient
from IPython import embed
from bs4 import BeautifulSoup
from selenium import webdriver

import unicodedata
import requests
import zipfile
import urllib
import json
import time
import itertools
import pysrt
import pickle
import re

def srt_to_text(srt):
    subs = pysrt.from_string(srt)
    text = [ s.text for s in subs]
    return " ".join(text)

class CourseraCrawler:
    DB_URI = 'mongodb://ir_final:irfinal2017@ds141098.mlab.com:41098/ir_final'
    COURSERA_URL = 'https://www.coursera.org'
    db = None
    collection = None
    course_links = None

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver')
        # client = MongoClient(self.DB_URI)
        # self.db = client.ir_final
        # self.collection = self.db.get_collection('cou_courses')

    def get_course_list(self):
        URL = "https://www.coursera.org/courses?_facet_changed_=true&domains=computer-science&primaryLanguages=en&query=computer+science&limit=300"
        response = requests.get(URL).text
        soup = BeautifulSoup(response,'html.parser')
        all_course = soup.find_all("a",class_="rc-OfferingCard")
        links = [ x['href'] for x in all_course  ]
        links = [ x for x in links if '/learn/' in x ]
        self.course_links = links
        # courses = soup.find_all("table",class_="courseList")[0].find_all('a',class_='preview')
        # self.course_links = [ x['href'] for x in courses ]
        # self.course_links = list(set(self.course_links))

    def login(self):
        self.driver.get(self.COURSERA_URL)
        login_btn = self.driver.find_element_by_css_selector('li.c-ph-right-nav-button.c-ph-log-in')
        login_btn.click()
        self.driver.find_element_by_name('email').send_keys('dondonb01501085@gmail.com')
        self.driver.find_element_by_name('password').send_keys('irfinal2017')
        self.driver.find_element_by_name('password').submit()
    def get_single_course_all_syllabus(self,course_url):
        course_url = self.COURSERA_URL + course_url + '?authMode=login' 
        
        #driver = webdriver.Chrome(executable_path=r'./chromedriver')
        self.driver.get(course_url)
        print(course_url)
        try:
            btn = self.driver.find_element_by_css_selector('div.toggle-button-wrapper')
            btn.click()
        except:
            print('cant click open')
        # try:
        #     element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By., "."))
        #     )
        # finally:
        #     driver.quit()
        time.sleep(1)
        elements = self.driver.find_elements_by_xpath("//button[contains(text(),'expand')]")
        elements += self.driver.find_elements_by_xpath("//button[contains(text(),'more')]")
        for e in elements:
            try:
                e.click()
                time.sleep(0.5)
            except:
                pass
            # finally:
                # print('no click')
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        course_title = soup.find_all('h1')[0].text
        lessons = soup.find_all('div',class_='module-name headline-2-text')
        print('Course %s' % (course_title),end='\r')
        course = {'title':course_title,'url':course_url,'lessons':[]}
        for lesson in lessons:
            lesson_hash = {}
            lesson_hash['name'] = unicodedata.normalize("NFKD", lesson.text) 
            lesson_hash['desc'] = unicodedata.normalize("NFKD", lesson.find_next(class_="module-desc").text) 
            materials = lesson.find_next(class_="rc-ModuleSummary").find_all('span',class_="item-name")
            for m in materials:
                if "Video" in m.find(class_="body-2-text").text:
                    lesson_hash['desc'] += " " + m.find(class_="body-1-text").text
            course['lessons'].append(lesson_hash)
        with open('coursera/'+course_title.replace('/',' '),'wb') as f:
            pickle.dump(course,f)

crawler = CourseraCrawler()
crawler.login()
crawler.get_course_list()
for course in crawler.course_links:
    time.sleep(1)
    crawler.get_single_course_all_syllabus(course)
