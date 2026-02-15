import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
#define set of stop words in the english language
STOPWORDS = set(stopwords.words("english"))


"""
    preprocessing.py help us to preprocess the dataset we obtained by apply lower case to any word,
    by removing puntuaction or any symbol that doesn't give us useful information.
    Stop words will be removed too.
"""


def preprocess_text(text):
    text = text.lower()

    #remove puntuactions and any other not meaningful words.
    text = re.sub(r"[^a-z\s]", " ", text)

    # tokenization by white space
    tokens = text.split()

    # remove all stopwords defined 
    tokens = [t for t in tokens if t not in STOPWORDS]

    return " ".join(tokens)