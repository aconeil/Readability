import os
import sqlite3
import random
from mle5 import mle
from xbox import best_rankings

def load_sentences(iso):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, ("../../sentences/" + iso + ".tsv")), 'r') as fin:
                return [x.split('\t') for x in fin.readlines()]

def run_xbox():
        #iso_codes = ["ca", "fi", "sw", "ru", "en", "es"]
        #open the language's database and get all the information
        iso_codes = ["en"]
        for iso in iso_codes:
                print(iso)
                con = sqlite3.connect('results.db')
                cur = con.cursor()
                comparisons = []
                sentences = []
                #fetch all of the comparisons for one of the iso codes
                raw_comparisons = cur.execute("SELECT comparison FROM "+iso+"judgements").fetchall()
                #append the comparisons from the file into list comparisons
                sentence_data = load_sentences(iso)
                for sentence in sentence_data:
                        #print(sentence)
                        sentences.append(sentence[2])
                for comparison in raw_comparisons:
                        csv_values = comparison[0]
                        values = csv_values.split(",")
                        values[0], values[1] = int(values[0]), int(values[1])
                        comparisons.append(values)
                #pass sentences and comparisons to mle2 code to get means and covariance matrix
                m, c = mle(comparisons, sentences)
                #print(m, c)
                #get sorted list of best sentences to compare
                relevance, sent_rankings = best_rankings(m, c)
                for ranking in sent_rankings:
                    ranking[2] = sentences[ranking[2]]
                    print(ranking)
                con.close()
        return

run_xbox()
