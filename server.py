import os
from flask import Flask
from flask import render_template
from flask import request
from time import time
from flask import abort, redirect, url_for

from abbreviation import Abbreviate
from lookup import Lookup

app = Flask(__name__)
lookup = Lookup(load_pickle=True)

def before_request():
    app.jinja_env.cache = {}

@app.route("/")
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/search_init', methods=['GET', 'POST'])
def search_init():
    if request.method == 'POST':
        abv = Abbreviate()
        de_abv_list = abv.run_deabbreviate(request.form['keyword'])
        if len(de_abv_list) == 0:
            return redirect(url_for('search',q=request.form['keyword']))
        else:
            return render_template('confirm.html',de_abv_list=de_abv_list,keyword=request.form['keyword'])
    else:
        return render_template('index.html')

@app.route('/search')
def search():
    if request.method == 'GET':
        keyword = request.args.get('q')
        # lesson_list = [{'course_name':'','lesson_name':'','youtube_id':''}]
        lesson_list = lookup.retrieve(keyword)
        print(lesson_list)
        return render_template('results.html',keyword=keyword,lesson_list=lesson_list)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.before_request(before_request)
    app.config.update(
        DEBUG=True,
        TESTING=True,
        TEMPLATES_AUTO_RELOAD=True
    )
    app.run(debug=True, host='0.0.0.0')
