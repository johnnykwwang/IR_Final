from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from WikiCrawler import WikiCrawler
from pycaption import *
from pycaption import transcript
# from pycaption.base import CaptionConverter
from pycaption.base import BaseWriter, CaptionNode
import pickle
from IPython import embed
import numpy as np
import re
import string
import pickle

class Lookup:
    clf = None
    count_vect = None
    tfidf_transformer = None

    def __init__(self,load_pickle=True):
        if load_pickle:
            f = open('classifier-pickle','rb')
            self.clf = pickle.load(f)
            f = open('count-vect-pickle','rb')
            self.count_vect = pickle.load(f)
            f = open('tfidf-transformer','rb')
            self.tfidf_transformer = pickle.load(f)

    def stem_tokens(self,tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tokenize(self,text):
        text = "".join([ch for ch in text if ch not in string.punctuation])
        text = "".join([ch for ch in text if ch in string.printable])
        tokens = word_tokenize(text)
        stemmer = PorterStemmer()
        stems = self.stem_tokens(tokens, stemmer)
        return stems

    def retrieve(self, keywords=["Algorithms"], load_pickle=True):
        target_dir = './mit_course_subtitles'
        coursera_train = load_files(target_dir,load_content=True)
        if load_pickle:
            clf = self.clf
            count_vect = self.count_vect
            tfidf_transformer = self.tfidf_transformer
            target_dir = './mit_course_subtitles'
            coursera_train = load_files(target_dir,load_content=True)
            # f = open('classifier-pickle','rb')
            # clf = pickle.load(f)
            # f = open('count-vect-pickle','rb')
            # count_vect = pickle.load(f)
            # f = open('tfidf-transformer','rb')
            # tfidf_transformer = pickle.load(f)
        else:
            count_vect = CountVectorizer(tokenizer=self.tokenize, stop_words='english')
            X_train_counts = count_vect.fit_transform(coursera_train.data)
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
            clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, coursera_train.target)
            with open('classifier-pickle','wb') as f:
                pickle.dump([clf, count_vect, tfidf_transformer],f)
        # crawler = WikiCrawler()
        # defnition, words = crawler.get_definition(keywords)
        X_new_counts = count_vect.transform([keywords])
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predicted = clf.predict(X_new_tfidf)
        probs = clf.predict_proba(X_new_tfidf)
        n = 5
        best_n = np.argsort(probs, axis=1)[:,::-1][:,:n]
        print("{}=>".format(keywords))
        for categories in best_n:
            for category in categories:
                print(coursera_train.target_names[category])
            print('\n', end='')

if __name__ == '__main__':
    lkp = Lookup()
    # keywords = ["Data Structure"]
    keywords = ['algorithm and data structure', 'computer network','minimum spanning tree']
    for key in keywords:
        lkp.retrieve(keywords=key, load_pickle=True)

