import os
import sqlite3
import flask
import random
import ast

from mle2 import mle
from xbox import best_rankings

from werkzeug.middleware.proxy_fix import ProxyFix
app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1, x_port=1)
app.secret_key = "8763OCA"

@app.route('/', methods=['GET', 'POST'])
#participant is shown the irb approval form
def cookie():
        return flask.render_template('index.html')

@app.route('/setcookie', methods = ['GET', 'POST'])
#if the participant approved the irb form, they can select a language
def setcookie():
        if flask.request.method == 'POST':
                resp = flask.make_response(flask.render_template('language_selection.html', iso = flask.request.args.get('iso')))
                resp.set_cookie("irb", "yes")
                return resp
        if "irb" not in flask.request.cookies:
                return flask.redirect(flask.url_for('cookie'))

@app.route('/getlang')
#use language selection to pull up tsv file from lang and pass to lang route with iso code
def getlang():
        iso = flask.request.args.get('iso')
        flask.session["ranking"] = load_data(iso)
        return flask.redirect(flask.url_for('lang', iso=iso))

def load_sentences(iso):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, ("../../sentences/" + iso + ".tsv")), 'r') as fin:
                return [x.split('\t') for x in fin.readlines()]

#load in the hundred sentences from last session or choose 100 random if first session ever
def load_data(iso):
        best_hundred = []
        con = sqlite3.connect('results.db')
        cur = con.cursor()
        #if database table is empty, choose 100 random sentence pairs
        value = cur.execute("SELECT * FROM " + iso + "nexthundred").fetchone()
        if value == None:
                list = random.sample(range(1000), 200)
                for i in range(0, 200, 2):
                        best_hundred.append([0, list[i], list[i+1]])
        #else choose sentences pairs from database suggestions
        else:
                best_hundred = cur.execute("SELECT * FROM "+iso+"nexthundred").fetchall()
                print("fetched from database")
        return best_hundred

@app.route('/lang', methods=['GET', 'POST'])
#this function adds the judgements to the proper table in the database each time
def lang():
        if flask.request.method == 'POST':
                form = flask.request.form
                iso = form['iso']
                if form['easier'] == 'sent1id':
                        judgement = (form['sentence2'], form['sentence1'])
                                #this judgement should go into xbox df
                        # connect to database
                        con = sqlite3.connect('results.db')
                        # create cursor object
                        cur = con.cursor()
                        #append the judgement that sentence 1 is easier (i,j) where i is harder than j
                        cur.execute("INSERT INTO "+iso+"judgements VALUES (?);", [','.join(judgement)])
                        con.commit()
                else:
                        #save judgement to database as comparison
                        con = sqlite3.connect('results.db')
                        # create cursor object
                        cur = con.cursor()
                        # append the judgement that sentence 2 is easier (i,j) where i is harder than j
                        judgement = (form['sentence1'], form['sentence2'])
                        cur.execute("INSERT INTO "+iso+"judgements VALUES (?);", [','.join(judgement)])
                        con.commit()
        else:
                iso = flask.request.args.get('iso')
        ranking_list = flask.session["ranking"]
        #once user gets through sentences, show thanks screen
        if not ranking_list:
                return flask.render_template('thanks.html', iso=iso, data=load_sentences(iso))
        data = load_sentences(iso)
        ranking = ranking_list.pop()
        flask.session["ranking"] = ranking_list
        score, idone, idtwo = ranking[0], ranking[1], ranking[2]
        # render ranking template using the selected ids
        return flask.render_template('ranking.html', sentence1=data[idone][2], sent1id=data[idone][0],
                              sentence2=data[idtwo][2], sent2id=data[idtwo][0], iso=iso)

@app.route('/run_xbox', methods=['GET', 'POST'])
def run_xbox():
        form = flask.request.form
        data = ast.literal_eval(form['data'])
        iso = form['iso']
        comparisons = []
        sentences = []
        #make a list of the sentences from data
        for point in data:
                sentences.append(point[2])
        con = sqlite3.connect('results.db')
        cur = con.cursor()
        #open the language's database and get all the information
        raw_comparisons = cur.execute("SELECT comparison FROM "+iso+"judgements").fetchall()
        #append the comparisons from the file into list comparisons
        for comparison in raw_comparisons:
                csv_values = comparison[0]
                values = csv_values.split(",")
                values[0], values[1] = int(values[0]), int(values[1])
                comparisons.append(values)
        #pass sentences and comparisons to mle2 code to get means and covariance matrix
        m, c = mle(comparisons, sentences)
        print("finished mle part")
        #get sorted list of best sentences to compare
        xbox_choices = best_rankings(m, c)
        print("finished xbox part")
        #save this in db to open at beginning of next session
        best_hundred = xbox_choices[:99]
        #print(best_hundred)
        for ranking in best_hundred:
                cur.execute("INSERT INTO "+iso+"nexthundred VALUES (?, ?, ?);", (ranking[0], ranking[1], ranking[2]))
                con.commit()
        return flask.render_template("index.html")

if __name__  == "__main__":
        app.run(debug=True)
