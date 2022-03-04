import sqlite3
import flask
import random
sentences = []
with open("/home/aconeil/Readability/Readability/sentences/fi.tsv", "r") as in_file:
        for line in in_file:
                (length, text)=line.split('\t')
                sentences.append(text)
        data = in_file.readlines()
        data = [x.split('\t') for x in data]
app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
        if flask.request.method == 'POST':
                form = flask.request.form
                if form['harder'] == '1':
                        print('Sentence 1 was harder')
                else:
                        print('Sentence 2 was harder')
                con = sqlite3.connect('results.db')
                cur = con.cursor()
                cur.execute("insert into judgements values (?, ?, ?)", (form['sentence1'], form['sentence2'], int(form['harder']) ))
                con.commit()
                return flask.redirect("/")
        else:
                mysentences = random.sample(sentences, k=2)
                return flask.render_template('ranking.html', sentence1 = mysentences[0], sentence2 = mysentences[1])

if __name__  == "__main__":
        app.run(debug=True)

