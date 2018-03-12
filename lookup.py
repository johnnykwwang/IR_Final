from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
# from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import LSHForest
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from WikiCrawler import WikiCrawler
from pycaption import *
from pycaption.base import BaseWriter, CaptionNode
import pickle
import numpy as np
import re
import string
import pickle


class Lookup:
    clf = None
    count_vect = None
    tfidf_transformer = None

    def __init__(self, load_pickle=False):
        if load_pickle:
            f = open('classifier-all-pickle','rb')
            self.clf, self.count_vect, self.tfidf_transformer = pickle.load(f)

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

    def retrieve(self,keyword="Algorithms",load_pickle=True,return_timestamps=False):
        if load_pickle:
            clf = self.clf
            count_vect = self.count_vect
            tfidf_transformer = self.tfidf_transformer
            target_dir = './mit_course_subtitles'
            coursera_train = load_files(target_dir,load_content=True)
        else:
            count_vect = CountVectorizer(tokenizer=self.tokenize, stop_words='english')
            target_dir = './mit_course_subtitles'
            coursera_train = load_files(target_dir, load_content=True)
            X_train_counts = count_vect.fit_transform(coursera_train.data)
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
            # clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, coursera_train.target)
            # clf = NearestNeighbors(n_neighbors=5, radius=1.0, algorithm='ball_tree', leaf_size=30, metric='cosine', p=2, metric_params=None, n_jobs=-1)
            clf = LSHForest(random_state=42).fit(X_train_tfidf, coursera_train.target)
            f = open('classifier-all-pickle','wb')
            pickle.dump([clf,count_vect,tfidf_transformer],f)
        crawler = WikiCrawler()
        # defnition, words = crawler.get_definition('algorithm')
        X_new_counts = count_vect.transform([keyword])
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        # probs = clf.predict_proba(X_new_tfidf)
        # print(np.percentile(probs[0],1))
        # n = 5
        # best_n = np.argsort(probs,axis=1)[:,::-1][:,:n]
        _, result  = clf.radius_neighbors(X_new_tfidf, 1)
        retrieved = []
        # for category in best_n[0]:
        for category in result[0]:
            try:
                doc_id = coursera_train.target.tolist().index(category)
                filename = coursera_train.filenames[doc_id]
                youtube_id = re.findall(r"(.{11}).en.vtt.txt",filename)[0]
                time_stamps = []
                vtt_file=""
                if return_timestamps:
                    vtt_filenames = filename.split('/')
                    vtt_filenames[1] = vtt_filenames[1] + "_vtt"
                    course_folder_name = re.findall(r"\[(.+)\] (.+)",vtt_filenames[2])[0][0]
                    lesson_folder_name = re.findall(r"\[(.+)\] (.+)",vtt_filenames[2])[0][1] 
                    vtt_filenames[2] = course_folder_name + '/' + lesson_folder_name
                    vtt_filenames[3] = vtt_filenames[3][:-4] 
                    vtt_file = '/'.join(vtt_filenames)
                    converter = CaptionConverter()
                    converter.read(open(vtt_file).read(), WebVTTReader())
                    for cap in converter.captions.get_captions('en-US'):
                        if keyword.lower() in cap.get_text().lower():
                            time_stamps.append( { 'time': cap.start / 1000000, 'text': cap.get_text() ,'contains': True} )
                        else:
                            time_stamps.append( { 'time': cap.start / 1000000, 'text': cap.get_text() ,'contains': False} )
                h = {'lesson_name':coursera_train.target_names[category],'filename':filename,'youtube_id':youtube_id,'vtt_file':vtt_file,'time_stamps':time_stamps}
                retrieved.append(h)
            except Exception:
                pass
        return retrieved


if __name__ == '__main__':
    lkp = Lookup(load_pickle=False)
    keywords = ["algorithms", "Data Structure"]
    for keyword in keywords:
        print(keyword)
        result = lkp.retrieve(keyword=keyword, load_pickle=False)
        for i in range(len(result)):
            print(result[i]['lesson_name'])
        print('\n',end='')