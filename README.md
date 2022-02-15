# Text difficulty classification

## Data

Data files are found in `sentences/`

| Language | File     | Buckets | Sentences/bucket | Checked | 
|----------|----------|---------|------------------|---------|
| Spanish  | `es.tsv` | 10      | 100              |  ✔      | 
| Catalan  | `ca.tsv` |         |                  |         |
| English  | `en.tsv` |         |                  |         |
| Russian  | `ru.tsv` |         |                  |         |
| Swahili  | `sw.tsv` |         |                  |         |
| Finnish  | `fi.tsv` |         |                  |         |

### Criteria for sentence selection

Sentences in the list are removed when:  
*Length is one token and the one token is a name  
*Two subsequent tokens in the sentence are the name of a person  
  *Written titles like "king" and "mister" in the language do not count
*Onomatopoeic expressions that aren't standardized in the language  
*The sentence is a fragment followed by an ellipses and meant to indicate trailing thought
