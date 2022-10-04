import sqlite3
import flask
import random
sentences = []

from werkzeug.middleware.proxy_fix import ProxyFix
app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1, x_port=1)

@app.route('/', methods=['GET', 'POST'])
def cookie():
        return flask.render_template('index.html')

@app.route('/setcookie', methods = ['GET', 'POST'])
def setcookie():
        if flask.request.method == 'POST':
                resp = flask.make_response(flask.render_template('language_selection.>
                resp.set_cookie("irb", "yes")
                return resp
#       print(flask.request.cookies)
#       check = flask.request.cookies.get(resp)
#       if "irb" not in check:
        if "irb" not in flask.request.cookies:
                return flask.redirect(flask.url_for('cookie'))
#       return flask.render_template('language_selection.html', id = flask.request.ar>
        return resp

#@app.route('/readability/getcookie')
#def getcookie():
#       name = flask.request.cookies.get('irb')
#       return f'The Cookie is set.'

@app.route('/lang', methods=['GET', 'POST'])
def lang():
#       for i in range(0,100):
        print(flask.request.headers['X-Forwarded-Prefix'])
        id = flask.request.args.get('id')
        if "irb" not in flask.request.cookies:
#               continue
#       else:
                return flask.redirect(flask.url_for('cookie'))
        if flask.request.method == 'POST':
                form = flask.request.form
                if form['harder'] == '1':
                        print('Sentence 1 was hard')
                else:
                        print('Sentence 2 was harder')
                con = sqlite3.connect('results.db')
                cur = con.cursor()
                cur.execute("insert into judgements values (?, ?, ?)", (form['sentenc>
                con.commit()
#               return flask.redirect(flask.url_for('index'))
#               print(id)
#               return flask.redirect(flask.url_for('lang', id=id))
        with open(("/home/aconeil/Readability/sentences/"+id+".tsv"), "r") as in_file:
#                       for line in in_file:
#                               (length, text)=line.split('\t')
#                               sentences.append(text)
                data = in_file.readlines()
                data = [x.split('\t') for x in data]
        mysentences = random.sample(data, k=2)
        return flask.render_template('ranking.html', sentence1 = mysentences[0][1], s>

if __name__  == "__main__":
        app.run(debug=True)
