import os
from flask import Flask
from flask import render_template
from flask import request
from time import time

from abbreviation import Abbreviate

app = Flask(__name__)

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
        return render_template('confirm.html',de_abv_list=de_abv_list,keyword=request.form['keyword'])
    else:
        return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        abv = Abbreviate()
        de_abv_list = abv.run_deabbreviate(request.form['keyword'])
        return render_template('confirm.html',de_abv_list=de_abv_list,keyword=request.form['keyword'])
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.before_request(before_request)
    app.config.update(
        DEBUG=True,
        TESTING=True,
        TEMPLATES_AUTO_RELOAD=True
    )
    app.run(debug=True, host='0.0.0.0')
