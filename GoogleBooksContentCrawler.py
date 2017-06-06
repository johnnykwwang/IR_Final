from bs4 import BeautifulSoup
import requests

class GoogleBooksContentCrawler:
    def __init__(self, urls):
        self.urls = urls

    def crawl(self):
        result = []
        for url in self.urls:
            r = requests.get(url).json()
            r = requests.get(r['volumeInfo']['previewLink'])
            soup = BeautifulSoup(r.text,'html.parser')
            chapters = []
            for e in soup.find_all('div', class_='toc_entry'):
                chapters.append(e.get_text())
            result.append(chapters)
        return result
            