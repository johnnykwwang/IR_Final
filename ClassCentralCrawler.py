from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

class ClassCentralCrawler:
    DB_URL = 'mongodb://ir_final:irfinal2017@ds155091.mlab.com:55091/ir_final'
    db = None
    collection = None

    def __init__(self):
        client = MongoClient(self.DB_URI)
        self.db = client.ir_final
        self.collection = self.db.get_collection('raw_courses')

    def parse(self,URL):
        response = requests.get(URL).text
        soup = BeautifulSoup(response,'html.parser')
        course_obj = {  'title': soup.h1.text, 
                        'description': soup.find_all("div",class_="course-desc")[0],
                        'link': soup.find_all("a", class_="cta-button btn_go_to_class")[0]['href'],
                        'taglist':  [ x.text.rstrip() for x in soup.find_all("div", class_="taglist")[0].find_all('a') ],
                        }

