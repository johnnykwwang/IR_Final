import os
from webvtt import WebVTT
from IPython import embed
from pycaption import *
from pycaption import transcript
from pycaption.base import BaseWriter, CaptionNode


def _strip_text(self, elements, lang_transcript):
    for el in elements:
        if el.type_ == CaptionNode.TEXT:
            lang_transcript += " "+el.content
    return lang_transcript


def recursive_walk(folder):
    converter = CaptionConverter()
    transcript.TranscriptWriter._strip_text = _strip_text
    for folderName, subfolders, filenames in os.walk(folder):
        # if subfolders:
        #     for subfolder in subfolders:
        #         recursive_walk(subfolder)
        # print('\nFolder: ' + folderName + '\n')
        for filename in filenames:
            root = folderName.split('/')[0]
            course_name = folderName.split('/')[1]
            lesson_name = folderName.split('/')[2]
            new_folderName = root+'/['+course_name+'] '+lesson_name
            print(folderName+"/"+filename)
            # embed()
            converter.read(open(folderName+'/'+filename).read(), WebVTTReader())
            script = converter.write(transcript.TranscriptWriter())
            if not os.path.exists(new_folderName):
                os.makedirs(new_folderName)
            f = open(new_folderName+'/'+filename+".txt", 'w')
            f.write(script)

recursive_walk('mit_course_subtitles')
