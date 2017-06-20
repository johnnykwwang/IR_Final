from IPython import embed
from bs4 import BeautifulSoup
import requests
import urllib
import json
import time
import itertools
import pickle
import re

class WikiCrawler:
    def __init__(self):
        pass

    def get_definition(self,keyword=""):
        url = "https://en.wikipedia.org/w/index.php?search="+keyword+"&title=Special%3ASearch&go=Go"
        response = requests.get(url).text
        soup = BeautifulSoup(response,'html.parser')
        definition = soup.find('div',class_="mw-body").find_all('p')[0].text
        no_ext_link_re = re.compile("\[\d+\]")
        words = [ a.text for a in soup.find('div',class_="mw-body").find_all('p')[0].find_all('a') if not no_ext_link_re.match(a.text) ]

        return definition,words

crawler = WikiCrawler()
embed()
