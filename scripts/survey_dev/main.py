#import numpy
import os
import sqlite3
import flask
import random
import ast

sentences = []

#from xbox import run_xbox

from werkzeug.middleware.proxy_fix import ProxyFix
app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1, x_port=1)


@app.route('/', methods=['GET', 'POST'])
def cookie():
        return flask.render_template('index.html')

@app.route('/setcookie', methods = ['GET', 'POST'])
def setcookie():
        if flask.request.method == 'POST':
                resp = flask.make_response(flask.render_template('language_selection.html', iso = flask.request.args.get('iso')))
                resp.set_cookie("irb", "yes")
                return resp
        if "irb" not in flask.request.cookies:
                return flask.redirect(flask.url_for('cookie'))

@app.route('/getlang')
def getlang():
        # sentences equal a random list of 100 integers in the range 0-10000
        # sentences = numpy.random.randint(0, 10000, size=100)
        # comparisons are minimum value of i and j and maximum value of i and j for sentences at index t in the list
        # this should come from here
        # comparisons is a list of pairs (i, j) where i is harder than j
        # comparisons = [
        #    (min(i,j,key=lambda t: sentences[t]),max(i,j, key=lambda t: sentences[t]))
        #    #size equals 8 sets us to compare only 8 sentences?
        #    for i in numpy.random.randint(0, len(sentences), size=8)
        #    for j in numpy.random.randint(0, len(sentences), size=8) if i != j
        # ]
        path = os.path.dirname(os.path.abspath(__file__))
        iso = flask.request.args.get('iso')
        in_file = open(os.path.join(path, ("../../sentences/" + iso + ".tsv")), "r")
        data_bulk = in_file.readlines()
        data = [x.split('\t') for x in data_bulk]
        return sentenceselect(data, iso)

def sentenceselect(data, iso):
        sentpair = random.sample(data, k=2)
        #print(sentpair)
        return flask.render_template('ranking.html', sentence1=sentpair[0][2], sent1id=sentpair[0][0],
                                     sentence2=sentpair[1][2], sent2id=sentpair[1][0], data=data, iso=iso)
@app.route('/lang', methods=['GET', 'POST'])
def lang():
        if flask.request.method == 'POST':
                form = flask.request.form
                if form['easier'] == 'sent1id':
                                #this judgement should go into xbox df
                        # connect to database
                        con = sqlite3.connect('results.db')
                        # create cursor object
                        cur = con.cursor()
                        #append the judgement that sentence 1 is easier (i,j) where i is harder than j
                        cur.execute("insert into judgements values (?, ?)", (("(" +form['sentence2'] + "," + form['sentence1'] + ")"), form['iso']))
                        con.commit()
                else:
                        #save judgement to database as comparison
                        con = sqlite3.connect('results.db')
                        # create cursor object
                        cur = con.cursor()
                        # append the judgement that sentence 2 is easier (i,j) where i is harder than j
                        cur.execute("insert into judgements values (?, ?)", (("(" + form['sentence1'] + "," + form['sentence2'] + ")"), form['iso']))
                        con.commit()
                #this should be loaded in each time to update the comparisons
                #comparisons = [(1,2), (3,2), (1,4)]
                #this needs to return updated value for covariance and mean of each sentence and sorted list?
                #run_xbox(sentences, comparisons)
                data = ast.literal_eval(form['data'])
        return sentenceselect(data, form['iso'])

# each time the page is loaded it grabs two sentences from the language tsv file
# read in judgements from the database and produce "comparisons" datastructure
# run xbox with sentences + comparisons, storing the result in res
# random sample with weighted coin flip from the covariance matrix for sentence--sentence (?)
# this should be selected by xbox, currently it is taking any two random values in the data

if __name__  == "__main__":
        app.run(debug=True)
