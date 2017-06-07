import sys


import ClassCentralCrawler

WARN = "warning"
TITLE = "title"
BODY = "body"

def classify(line):
    if line.startwith("###"):
        return WARN
    elif line.startwith("##"):
        return TITLE
    else:
        return BODY


def separate_by_colom(line):
    return line.split(",")


def crawl_courses(filename, db=None):
    if db is None:
        db = ClassCentralCrawler()

    with open(filename, "r") as f:
        for line in f.readlines():
            cate = classify(line)
            if cate == BODY:
                url = separate_by_colom(line)
                print("Crawling url: {}".format(url))
                db.parse(url)

    return


def main():
    filename = sys.argv[1]
    print("Reading from {}".format(filename))
    return
    db = ClassCentralCrawler()
    crawl_courses(filename, db)




if __name__ == "__main__":
    main()
