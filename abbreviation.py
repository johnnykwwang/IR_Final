import sys
from xml.etree import ElementTree as ET

import requests


class Abbreviate:

    abbreviation_url = [
        'http://www.stands4.com/services/v2/abbr.php',
    ]
    uid = 5812
    tid = '1I3AHWHDOvS3SSX7'

    def __init__(self):
        pass

    def accept_query_term(self):
        term = input("Enter the query term: ")
        self.query_term = term

    def de_abbreviation(self, term=None, cate_id='all'):
        if term is None:
            term = self.query_term


        payload = {
            'sortby': 'p',
            'term': term,
            'categorid': cate_id,
            'uid': self.uid,
            'tokenid': self.tid,
            'searchtype': 'e'
        }
        
        response = requests.get(self.abbreviation_url[0], params=payload)
        return response.content

    def parse_abb_response(self, response, cate=None):
        # parse the response from www.abbreivations.com
        root = ET.fromstring(response)
        result = []
        for each_result in list(root):
            for tag in list(each_result):
                if tag.tag == 'definition':
                    result.append(tag.text)
        return result
        
    def run_deabbreviate(self, term=None):
        if term is None:
            self.accept_query_term()
        else:
            self.query_term = term

        response = self.de_abbreviation()
        results = self.parse_abb_response(response)
        return results


def main():
    try:
        term = sys.argv[1]
    except Exception:
        term = None

    a = Abbreviate()
    results = a.run_deabbreviate(term)
    print(results)
    return results


if __name__ == '__main__':
    main()

