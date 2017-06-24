from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from WikiCrawler import WikiCrawler
import numpy as np
import string
import pickle

class Lookup:
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
        # return tokens

    def retrieve(self,keyword="Algorithms",load_pickle=True):
        clf = None
        if load_pickle:
            f = open('classifier-pickle','rb')
            clf = pickle.load(f)
        else:
            tfidf_transformer = TfidfTransformer()
            target_dir = './mit_course_subtitles'
            coursera_train = load_files(target_dir,load_content=True)
            count_vect = CountVectorizer(tokenizer=self.tokenize, stop_words='english')

            X_train_counts = count_vect.fit_transform(coursera_train.data)
            # print(count_vect.get_feature_names())
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
            #clf = MultinomialNB().fit(X_train_tfidf, coursera_train.target)
            clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, coursera_train.target)
            f = open('classifier-pickle','wb')
            pickle.dump(clf,f)
        crawler = WikiCrawler()
        defnition,words = crawler.get_definition('algorithm')
        docs_new = [ keyword ]
        # docs_new = ['algorithm and data structure', 'computer network','minimum spanning tree']
        X_new_counts = count_vect.transform(docs_new)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predicted = clf.predict(X_new_tfidf)
        probs = clf.predict_proba(X_new_tfidf)
        print(len(probs[0]))
        for doc, category in zip(docs_new, predicted):
            print('%r => %s' % (doc, coursera_train.target_names[category]))

if __name__ == '__main__':
    lkp = Lookup()
    lkp.retrieve(keyword="Data Structure",load_pickle=False)
