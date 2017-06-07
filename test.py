import unittest
from GoogleBooksContentCrawler import *
from GoogleBooksSearcher import *

class TestGoogleBooksContentCrawer(unittest.TestCase):
    def test_crawel(self):
        urls = ['https://www.googleapis.com/books/v1/volumes/zyTCAlFPjgYC']
        gbcc = GoogleBooksContentCrawler(urls)
        result = gbcc.crawl()
        self.assertEqual(result, [['Introduction', 'CHAPTER 1A Healthy Disregard for the Impossible', 
        'CHAPTER 2When Larry Met Sergey', 'CHAPTER 3Learning to Count', 'CHAPTER 4The Secret Sauce',
        'CHAPTER 5Divide and Conquer', 'CHAPTER 6Burning Man', 'CHAPTER 7The Danny Sullivan Show',
        'CHAPTER 17Playboys', 'CHAPTER 18Charlies Place', 'CHAPTER 19Space Race', 'CHAPTER 20A Legal Showdown',
        'CHAPTER 21A Virtual Library', 'CHAPTER 22Trick Clicks', 'CHAPTER 23Attacking Microsoft',
        'CHAPTER 24Money Machine', 'CHAPTER 8A Trickle', 'CHAPTER 9Hiring a Pilot', 'CHAPTER 10Youve Got Google',
        'CHAPTER 11The Google Economy', 'CHAPTER 12And on the Fifth Day\xa0', 'CHAPTER 13Global Goooogling',
        'CHAPTER 14April Fools', 'CHAPTER 15Porn Cookie Guy', 'CHAPTER 16Going Public', 'CHAPTER 25The China Syndrome',
        'CHAPTER 26Googling Your Genes', 'APPENDIX I23 Google Search Tips', 'Appendix II',
        'APPENDIX IIIGoogles Financial Scorecard', 'A Note on Sources', 'Acknowledgments', 'Photo Credits', '版權所有']])

class TestGoogleBooksSearcher(unittest.TestCase):
    def test_search(self):
        book_names = ['Computer Network']
        gbs = GoogleBooksSearcher(book_names)
        result = gbs.search()
        self.assertEqual(result, ['https://www.googleapis.com/books/v1/volumes/BvaFreun1W8C'])

if __name__ == '__main__':
    unittest.main()
