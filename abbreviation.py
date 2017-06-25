import sys
from xml.etree import ElementTree as ET

import requests


class Abbreviate:

    abbreviation_url = [
        'http://www.stands4.com/services/v2/abbr.php',
    ]
    uid = 5812
    tid = '1I3AHWHDOvS3SSX7'
    freq_used_cat = [
        'computing', 'assembly', 'security',
        'databases', 'dos', 'drivers',
        'fileext', 'gaming', 'general',
        'hardware', 'java', 'networking',
        'software', 'technology', 'telecom'
        'texting', 'unix',
    ]

    def __init__(self):
        pass

    def accept_query_term(self):
        term = input("Enter the query term: ")
        self.query_term = term

    def de_abbreviation(self, term=None, cate_id=None):
        if term is None:
            term = self.query_term


        payload = {
            'sortby': 'p',
            'term': term,
            'categoryid': cate_id,
            'uid': self.uid,
            'tokenid': self.tid,
            'searchtype': 'e'
        }
        
        response = requests.get(self.abbreviation_url[0], params=payload)
        return response.content

    def parse_abb_response(self, response, cate=None):
        if cate is None:
            cate = self.freq_used_cat

        # parse the response from www.abbreivations.com
        root = ET.fromstring(response)
        result = []
        for each_result in list(root):
            tmp = {}
            for tag in list(each_result):
                if tag.tag == 'definition':
                    tmp['def'] = tag.text
                elif tag.tag == 'category':
                    tmp['cat'] = tag.text.lower()
            if cate is not None:
                if tmp['cat'] in cate:
                    result.append(tmp['def'])
            else:
                result.append(tmp['def'])
        return result
        
    def run_deabbreviate(self, term=None, cate=None):
        if term is None:
            self.accept_query_term()
        else:
            self.query_term = term

        response = self.de_abbreviation()
        results = self.parse_abb_response(response, cate)
        return results


def main():
    try:
        term = sys.argv[1]
    except Exception:
        term = None

    try:
        cate = sys.argv[2]
    except Exception:
        cate = None

    a = Abbreviate()
    results = a.run_deabbreviate(term, cate)
    print(results)
    return results


if __name__ == '__main__':
    main()

