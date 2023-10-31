# unicode, regex, json for text digestion
import unicodedata
import re
import json

# nltk: natural language toolkit -> tokenization, stopwords
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import acquire
from time import strftime

# This function takes in a string and returns the string normalized
def basic_clean(string):
    # we will normalize our data into standard NFKD unicode, feed it into an ascii encoding
    # decode it back into UTF-8
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    # remove special characters, then lowercase
    string = re.sub(r"[^\w0-9'\s]", '', string).lower()
    return string

# This functions takes in a string and returns a tokenized string
def tokenize(string):
    # make our tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # apply our tokenization to the string input
    string = tokenizer.tokenize(string, return_str = True)
    return string

# This function takes in a string and returns a string with words stemmed
def stem(string):
    # create our stemming object
    ps = nltk.porter.PorterStemmer()
    # use a list comprehension => stem each word inside of the entire document and split by single spaces
    stems = [ps.stem(word) for word in string.split()]
    # join it together with spaces
    string = ' '.join(stems)
    
    return string

# This function takes in a string  and returns a string with words lemmatized
def lemmatize(string):
    # create our lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    # use a list comprehension to lemmatize each word
    # string.split() => output a list of every token inside of the document
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # join the lemmas together with spaces
    string = ' '.join(lemmas)
    #return the altered document
    return string

# This function takes in a string, optional extra_words and exclued_words parameters with default empty lists and returns a string
def remove_stopwords(string, extra_words = [], exclude_words = []):
    stopword_list = stopwords.words('english')
    # use set casting to remove any excluded stopwords
    stopword_set = set(stopword_list) - set(exclude_words)
    # add in extra words to stopwords set using a union
    stopword_set = stopword_set.union(set(extra_words))
    # split the document by spaces
    words = string.split()
    # every word in our document that is not a stopword
    filtered_words = [word for word in words if word not in stopword_set]
    # join it back together with spaces
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords

def clean(string, extra_stopwords):    
    words = remove_stopwords((tokenize(basic_clean(string))), extra_stopwords)
    return words