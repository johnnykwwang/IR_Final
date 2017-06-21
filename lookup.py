from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from WikiCrawler import WikiCrawler
import numpy as np

crawler = WikiCrawler()
tfidf_transformer = TfidfTransformer()
coursera_train = load_files('./coursera-cat',load_content=True)
count_vect = CountVectorizer(stop_words='english', ngram_range=(1,2))

X_train_counts = count_vect.fit_transform(coursera_train.data)
print(count_vect.get_feature_names())
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#clf = MultinomialNB().fit(X_train_tfidf, coursera_train.target)
clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, coursera_train.target)
docs_new = []

defnition,words = crawler.get_definition('algorithm')
query = 'singular value decomposition'
print(query)
docs_new.append(query)
#docs_new = ['algorithm and data structure', 'computer network','minimum spanning tree']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
probs = clf.predict_proba(X_new_tfidf)
print(len(probs[0]))
for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, coursera_train.target_names[category]))
