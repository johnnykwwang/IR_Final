# from __future__ import unicode_literals
import youtube_dl
from IPython import embed

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

ydl_opts = {
    # 'logger': MyLogger(),
    'writesubtitles': 'True',
    'skip_download': 'True',
    # 'outtmpl': 'mit_course_transcript/%(playlist_title)s/%(title)s-%(id)s.%(ext)s'
    'outtmpl': 'mit_course_subtitles/%(playlist_title)s/%(title)s/%(title)s-%(id)s.%(ext)s'
}

with open("mit-yt-list", encoding="utf-8") as f:
    yt_list = f.readlines()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        r = ydl.download(yt_list)
