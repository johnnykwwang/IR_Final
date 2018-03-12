from pymongo import MongoClient
from IPython import embed
from bs4 import BeautifulSoup
import requests
import json
import itertools
import pysrt
import pickle
import re


def srt_to_text(srt):
    subs = pysrt.from_string(srt)
    text = [ s.text for s in subs]
    return " ".join(text)


class MITCrawler:
    DB_URI = 'mongodb://ir_final:irfinal2017@ds141098.mlab.com:41098/ir_final'
    MIT_URL = 'https://ocw.mit.edu'
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
        soup = BeautifulSoup(response, 'html.parser')
        courses = soup.find_all("div", class_="courseListDiv")[0].find_all('a',class_='preview')
        self.course_links = [ x['href'] for x in courses ]
        self.course_links = list(set(self.course_links))

    def get_course_with_transcript(self):
        base_URL = "https://ocw.mit.edu"
        course_with_transcript = []
        for x in self.course_links:
            json_url = base_URL + x + '/index.json'
            res = requests.get(json_url).text
            j = json.loads(res)
            if 'transcript' in j['features']:
                course_with_transcript.append(x)

    def parse(self, URL):
        response = requests.get(URL).text
        soup = BeautifulSoup(response,'html.parser')
        course_obj = {  'title': soup.h1.text, 
                        'description': str(soup.find_all("div",class_="course-desc")[0]),
                        'link': soup.find_all("a", class_="cta-button btn_go_to_class")[0]['href'],
                        'taglist':  [ x.text.rstrip() for x in soup.find_all("div", class_="taglist")[0].find_all('a') ],
                        }
        self.collection.insert_one(course_obj)

    def get_single_course_all_transcript(self,course_url):
        course_url = self.MIT_URL + course_url 
        response = requests.get(course_url).text
        soup = BeautifulSoup(response, 'html.parser')
        course_title = soup.find_all('h1')[0].text
        units = soup.find_all('div',class_='tlp_links')
        lessons = [u.select('li a') for u in units ]
        lessons_all = list(itertools.chain.from_iterable(lessons))
        course_h = {'url':course_url, 'title': course_title, 'lessons': []}
        lessons_all = [ {'link': les['href'], 'name': les.text } for les in lessons_all ]
        for lesson in lessons_all:
            try:
                print('Class %s' % (lesson['name']),end='\r')
                lesson_url = self.MIT_URL + lesson['link']
                response = requests.get(lesson_url).text
                soup = BeautifulSoup(response,'html.parser')
                srt_link = soup.find_all('a',class_='poplink',href=re.compile('\.srt'))[0]['href']
                response = requests.get(self.MIT_URL+srt_link).text
                transcript = srt_to_text(response).replace('\n',' ')
                lesson['script'] = transcript
            except IndexError:
                print('quiz or srt not found')
                embed()
            except KeyError:
                print('Lesson error')
        # self.collection.insert({'course_title':course_title,'lessons':lessons_all})
        course_h['lessons'] = lessons_all
        print(lessons_all)
        with open('mit-courses-transcript/'+course_title.replace('/',' '),'wb+') as f:
            pickle.dump(lessons_all, f)


if __name__ == '__main__':
    USE_OLD_LIST = True

    crawler = MITCrawler()
    if USE_OLD_LIST:
        crawler.get_course_list()
    else:
        crawler.course_links = pickle.load(open('mit-course-with-transcript', 'rb'))
    for course in crawler.course_links:
        crawler.get_single_course_all_transcript(course)
    # crawler.get_course_with_transcript()
