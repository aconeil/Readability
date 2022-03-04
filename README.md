# Text difficulty classification

## Data

Data files are found in `sentences/`

| Language | File     | Buckets | Sentences/bucket | Checked | 
|----------|----------|---------|------------------|---------|
| Spanish  | `es.tsv` | 10      | 100              |  ✔      | 
| Catalan  | `ca.tsv` | 10      | 100              |  ✔      | 
| English  | `en.tsv` |         |                  |         |
| Russian  | `ru.tsv` |         |                  |         |
| Swahili  | `sw.tsv` |         |                  |         |
| Finnish  | `fi.tsv` | 10      | 100              |  ✔      | 

### Criteria for sentence selection

Sentences in the list are removed when:  
* Length is one token and the one token is a name  
* Two subsequent tokens in the sentence are the name of a person 
  * Written titles like "king" and "mister" in the language do not count
* The sentence is only an onomatopoeic expressions that isn't standardized in the language  
* The sentence is a fragment followed by an ellipses and meant to indicate trailing thought
* If there are many template sentences such as "Venim de `Toponym`"
* If proper names take up more than 50% of the sentence (e.g. 2/3 tokens, *Sigüenza i Guadalajara.*)
* Names of continents and countries are allowed, cities, rivers, and villages not.


### Tokenisation

Tokens are defined as space separated, thus a single token may consist
of two syntactic "words" when apostrophisation or contraction takes place, 
*del*, *that's*, *m'explico*.

Note that taking a sub-token definition would require counting clitic pronouns in Spanish
where they are written joined with the previous word, for example Catalan *dis-m'ho* vs. 
Spanish *dímelo* vs. English *say it to me*.

This only applies to those languages with contractions, e.g. English, Spanish and Catalan.

**TODO:** Check if this is the definition we want.


