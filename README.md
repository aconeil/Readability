# Text difficulty classification

## Survey Tool
The survey program can be found in `scripts/survey_dev`. Following the submission of the research consent form and selection of the language, this survey presents the participants with sentences in pairs and they are prompted to select which sentence in the pair easier. Upon selection, the next pair is rendered for the participant to provide a judgement on. Participants are asked to provide 100 judgements. Following the 100th judgement, a screen is presented that notifies participants that they have completed the survey and prompts them to submit the survey. Once they click submit, the submit button turns green and they can exit the program. The survey can be posted to the server using the following command: 
`FLASK_APP=main.py flask run`

Hitting the submit button executes the code that ranks the sentences using the TSSort method for Probabilistic Noise Resistance Sorting as outlined [here](https://www.arxiv-vanity.com/papers/1606.05289/). To use this method, the comparisons from the users are stored in the database `scripts/survey_dev/results.db` and then passed to the mle.py code to generate the mu and sigma score for each sentence. This information is then passed to the xbox.py code to generate a list of sentences that are ordered by which sentence pairs would be the next best for participants to rank.

## Data

Data files are found in `sentences/`

| Language | File     | Buckets | Sentences/bucket | Checked | 
|----------|----------|---------|------------------|---------|
| Spanish  | `es.tsv` | 10      | 100              |  ✔      | 
| Catalan  | `ca.tsv` | 10      | 100              |  ✔      | 
| English  | `en.tsv` | 10      | 100              |  ✔      |
| Russian  | `ru.tsv` | 10      | 100              |  ✔      |
| Swahili  | `sw.tsv` |         |                  |         |
| Finnish  | `fi.tsv` | 10      | 100              |  ✔      |
| Zulu     | `zu.tsv` |         |                  |         |

### Criteria for sentence selection

Sentences in the list are removed when:  
* Length is one token and the one token is a name  
* Two subsequent tokens in the sentence are the name of a person 
  * Written titles like "king" and "mister" in the language do not count
* The sentence is only an onomatopoeic expressions that isn't standardized in the language  
* The sentence is a fragment followed by an ellipses and meant to indicate trailing thought
* If there are many template sentences such as "Venim de `Toponym`"
* If proper names take up more than 50% of the sentence (e.g. 2/3 tokens, *Sigüenza i Guadalajara.*)
* Names of continents and countries are allowed, states, provices, cities, rivers, and villages not.
  * When the name is preceeded by the specificed place, such as "River `Name`" or "Lake `Name`" it remains in the corpus
* The sentence discusses mature subject matter or uses curse words
* One of the tokens is a link
* The sentence is an article title
* Non-standard punctuation may contribute to the sentence's difficulty
  * Such as lack of quotation marking *Mitä te sanotte Voiko niitä tarjota lehteen?*

### Tokenisation

Tokens are defined as space separated, thus a single token may consist
of two syntactic "words" when apostrophisation or contraction takes place, 
*del*, *that's*, *m'explico*, *покажи-ка*.

Note that taking a sub-token definition would require counting clitic pronouns in Spanish
where they are written joined with the previous word, for example Catalan *dis-m'ho* vs. 
Spanish *dímelo* vs. English *say it to me*.

This only applies to those languages with contractions, e.g. English, Spanish and Catalan.

### Sentence Data Sources

Sentence data has been taken from:

* [Wikimedia Downloads](https://dumps.wikimedia.org/backup-index.html)
* [OpenSubtitles](http://www.opensubtitles.org/)
* [The QCRI Educational Domain (QED) Corpus](https://alt.qcri.org/resources/qedcorpus/)


### Adding Language Data 
To generate additional data files for other languages the sample.py file found in `scripts/` can be used by feeding in a newline separated textfile, such as one generated using [WikiExtractor](https://github.com/apertium/WikiExtractor.git). To collect these sentences run the following command, replacing ISO with the ISO code of the language you are generating data for: `python3 sample.py < WikiExtractor/wiki.txt > ISO.tsv`

Once these sentences are generated, they should then be reviewed to ensure they follow the guidelines outlined above. Save the excluded sentences in `sentences/exclusions/` using the sample.py code as follows: `python3 sample.py old_file.tsv new_file.tsv > exclusions/ISO.tsv`


### Another thing

In order to use the script to get only sentences that have not been seen
and are not in the exclusions file, you can do the following:

```
cat sentences/ru.tsv | cut -f2- > /tmp/ru.tsv
cat /tmp/ru.subs | python3 scripts/sample.py /tmp/ru.tsv sentences/exclusions/ru.tsv >/tmp/newru.tsv
cat /tmp/newru.tsv | grep -v '\*' | cat -n | sed 's/^ *//g' > sentences/ru.tsv
diff -Naur /tmp/ru.tsv /tmp/newru.tsv | grep '^-' | sed 's/^-//g' >> sentences/exclusions/ru.tsv
```

This will give a file where there are new sentences that are marked
with `*` that can be checked.
