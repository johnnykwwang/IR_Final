import os
import pickle
from os import listdir
from os.path import isfile, join
import re

mypath = './coursera'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in onlyfiles:
    obj = pickle.load(open(mypath+'/'+f,'rb'))
    course_title = obj['title']
    for l in obj['lessons']:
        subname = re.sub('[^0-9a-zA-Z]+','_',l['name'])
        dir_name = re.sub('[^0-9a-zA-Z]+','_',course_title+ '_' + subname)
        dir_name = './coursera-cat/'+dir_name
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        w = open(dir_name + '/'+subname,'w')
        w.write(l['desc'])


