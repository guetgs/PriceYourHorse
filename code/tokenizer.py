import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


def tokenizer(s):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenizes string into list of words.
    '''
    token = word_tokenize(s.lower())
    stpw = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    clean = [w for w in token if w not in stpw and w not in exclude]
    wordnet = WordNetLemmatizer()
    lemmatized = [wordnet.lemmatize(word) for word in clean]
    return lemmatized
