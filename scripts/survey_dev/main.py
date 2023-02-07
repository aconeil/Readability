import os
import sqlite3
import flask
import random
from apscheduler.schedulers.background import BackgroundScheduler
from mle2 import mle
from xbox import best_rankings

from werkzeug.middleware.proxy_fix import ProxyFix
app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1, x_port=1)
app.secret_key = "8763OCA"

@app.route('/', methods=['GET', 'POST'])
#participant is shown the irb approval form and xbox function is set to run every 12 hours
def cookie():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=run_xbox, trigger='interval', hours=12)
        scheduler.start()
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
        return flask.render_template("level.html", iso=iso)

@app.route('/getlevel')
def getlevel():
        level = flask.request.args.get('level')
        iso = flask.request.args.get('iso')
        print("get level", level, iso)
        return flask.redirect(flask.url_for('lang', iso=iso, level=level))

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
                con.close()
                return best_hundred
        #if there are more than 100 that have 4 in the first column, make a subset of those to randomize and return
        else:
                #take results from the nexthundred table for the language
                nexthundred = cur.execute("SELECT * FROM "+iso+"nexthundred").fetchall()
                sparse_data = []
                ranked_data = []
                #go through the list of best_hundred sentences and make a list of the ranked data
                for sentence in nexthundred:
                        ranked_data.append(sentence)
                        #make a list of all of the sentences that have a score of 4 and append to sparse data list
                        if sentence[0] == 4.0:
                                sparse_data.append(sentence)
                #if there are more than 100 sentences ranked as 4, sample randomly to find next ones
                #figure out how to delete the randomly samples data from table
                #if there are less than 101 items in the list ranked data, sample randomly to create the list best_hundred
                if len(ranked_data) < 101:
                        list = random.sample(range(1000), 200)
                                for i in range(0, 200, 2):
                                    best_hundred.append([0, list[i], list[i+1]])
                                con.close()
                                return best_hundred
                #or is there are more than 100 values in sparse data randomly sample 100 of those
                elif len(sparse_data) > 100:
                        list = random.sample(range(len(sparse_data)), 100)
                        for i in range(0,100):
                                #print(sparse_data[list[i]])
                                best_hundred.append(sparse_data[list[i]])
                                #cur.execute("DELETE FROM " + iso + "nexthundred WHERE ")
                                #print(best_hundred)
                        return best_hundred
                #else choose the first hundred and delete those options from the database
                else:
                        for i in range(0,100):
                                best_hundred.append(ranked_data[i])
                        cur.execute("DELETE FROM " + iso + "nexthundred ORDER BY score LIMIT 100")
                        con.close()
                        return best_hundred

@app.route('/lang', methods=['GET', 'POST'])
#this function adds the judgements to the proper table in the database each time
def lang():
        if flask.request.method == 'POST':
                form = flask.request.form
                iso = form['iso']
                level = form['level']
                if form['easier'] == 'sent1id':
                        judgement = (form['sentence2'], form['sentence1'])
                        judgement = ','.join(judgement)
                        # connect to database
                        con = sqlite3.connect('results.db')
                        # create cursor object
                        cur = con.cursor()
                        #append the judgement that sentence 1 is easier (i,j) where i is harder than j
                        cur.execute("INSERT INTO "+iso+"judgements VALUES (?, ?);", (judgement, level))
                        con.commit()
                        con.close()
                else:
                        #save judgement to database as comparison
                        con = sqlite3.connect('results.db')
                        # create cursor object
                        cur = con.cursor()
                        # append the judgement that sentence 2 is easier (i,j) where i is harder than j
                        judgement = (form['sentence1'], form['sentence2'])
                        judgement = ','.join(judgement)
                        print(judgement, level)
                        cur.execute("INSERT INTO "+iso+"judgements VALUES (?, ?);", (judgement, level))
                        con.commit()
                        con.close()
        else:
                iso = flask.request.args.get('iso')
                level = flask.request.args.get('level')
        ranking_list = flask.session["ranking"]
        if not ranking_list:
                return flask.render_template(iso+'thanks.html', iso=iso, data=load_sentences(iso))
        data = load_sentences(iso)
        ranking = ranking_list.pop()
        flask.session["ranking"] = ranking_list
        score, idone, idtwo = ranking[0], ranking[1], ranking[2]
        # render ranking template using the selected ids
        return flask.render_template(iso+'ranking.html', sentence1=data[idone][2], sent1id=data[idone][0],
                              sentence2=data[idtwo][2], sent2id=data[idtwo][0], iso=iso, level=level)


#@app.route('/run_xbox', methods=['GET', 'POST'])
def run_xbox():
        # form = flask.request.form
        # data = ast.literal_eval(form['data'])
        # iso = form['iso']
        # comparisons = []
        # sentences = []
        # #make a list of the sentences from data
        # for point in data:
        #         sentences.append(point[2])
        iso_codes = ["ca", "fi", "sw", "ru", "en", "es"]
        #open the language's database and get all the information
        for iso in iso_codes:
                con = sqlite3.connect('results.db')
                cur = con.cursor()
                print("starting xbox for", iso)
                comparisons = []
                sentences = []
                #fetch all of the comparisons for one of the iso codes
                raw_comparisons = cur.execute("SELECT comparison FROM "+iso+"judgements").fetchall()
                #append the comparisons from the file into list comparisons
                sentence_data = load_sentences(iso)
                for sentence in sentence_data:
                        sentences.append(sentence[2])
                for comparison in raw_comparisons:
                        csv_values = comparison[0]
                        values = csv_values.split(",")
                        values[0], values[1] = int(values[0]), int(values[1])
                        comparisons.append(values)
                #pass sentences and comparisons to mle2 code to get means and covariance matrix
                m, c = mle(comparisons, sentences)
                print("finished mle part for", iso)
                #get sorted list of best sentences to compare
                xbox_choices = best_rankings(m, c)
                print("finished xbox part for", iso)
                xbox_choices_sample = xbox_choices[:5000]
                #save this in db to open at beginning of next session
                #print(best_hundred)
                for ranking in xbox_choices_sample:
                        cur.execute("DELETE FROM "+iso+"nexthundred")
                        cur.execute("INSERT INTO "+iso+"nexthundred VALUES (?, ?, ?);", (ranking[0], ranking[1], ranking[2]))
                        con.commit()
                con.close()
        return

if __name__  == "__main__":
        app.run(debug=True)
