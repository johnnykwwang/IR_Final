import sys


import ClassCentralCrawler

WARN = "warning"
TITLE = "title"
BODY = "body"

def classify(line):
    if line.startswith("###"):
        return WARN
    elif line.startswith("##"):
        return TITLE
    else:
        return BODY


def separate_by_colom(line):
    return line.split(",")


def crawl_courses(filename, db=None):
    if db is None:
        db = ClassCentralCrawler.ClassCentralCrawler()

    with open(filename, "r") as f:
        for line in f.readlines():
            cate = classify(line)
            if cate == BODY:
                url = separate_by_colom(line)[0]
                print("Crawling url: {}".format(url))
                db.parse(url)

    return


def main():
    filename = sys.argv[1]
    print("Reading from {}".format(filename))
    db = ClassCentralCrawler.ClassCentralCrawler()
    crawl_courses(filename, db)




if __name__ == "__main__":
    main()
