from pymongo import MongoClient
from IPython import embed
from bs4 import BeautifulSoup
import requests
import json

class MITCrawler:
    DB_URI = 'mongodb://ir_final:irfinal2017@ds141098.mlab.com:41098/ir_final'
    db = None
    collection = None
    course_links = None

    def __init__(self):
        client = MongoClient(self.DB_URI)
        self.db = client.ir_final
        self.collection = self.db.get_collection('mit_courses')

    def get_course_list(self):
        URL = "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/"
        response = requests.get(URL).text
        soup = BeautifulSoup(response,'html.parser')
        courses = soup.find_all("table",class_="courseList")[0].find_all('a',class_='preview')
        self.course_links = [ x['href'] for x in courses ]

    def get_course_with_transcript(self):
        base_URL = "https://ocw.mit.edu"
        course_with_transcript = []
        for x in self.course_links:
            json_url = base_URL + x + '/index.json'
            res = requests.get(json_url).text
            j = json.loads(res)
            if 'transcript' in j['features']:
                course_with_transcript.append(x)

    def parse(self,URL):
        response = requests.get(URL).text
        soup = BeautifulSoup(response,'html.parser')
        course_obj = {  'title': soup.h1.text, 
                        'description': str(soup.find_all("div",class_="course-desc")[0]),
                        'link': soup.find_all("a", class_="cta-button btn_go_to_class")[0]['href'],
                        'taglist':  [ x.text.rstrip() for x in soup.find_all("div", class_="taglist")[0].find_all('a') ],
                        }
        self.collection.insert_one(course_obj)

crawler = MITCrawler()
crawler.get_course_list()
crawler.get_course_with_transcript()
