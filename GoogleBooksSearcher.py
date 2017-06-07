import requests

class GoogleBooksSearcher:
    __BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

    def __init__(self, book_names):
        self.book_names = book_names

    def search(self):
        result = []
        for book_name in self.book_names:
            r = requests.get(self.__BASE_URL, params={'q':book_name}).json()
            result.append(r['items'][0]['selfLink'])
        return result
        