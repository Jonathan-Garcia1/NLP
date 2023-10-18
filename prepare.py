import pandas as pd

import unicodedata
import re

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

nltk.download('wordnet')


def basic_clean(data):
    # Convert the text to lowercase
    data = data.lower()
    
    # Normalize the text by removing any diacritical marks
    data = unicodedata.normalize('NFKD', data)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    
    # Remove any characters that are not lowercase letters, numbers, apostrophes, or whitespaces
    data = re.sub(r"[^a-z0-9'\s]", "", data)
    
    # Return the cleaned data
    return data


def tokenize(data):
    # Initialize a tokenizer object
    tokenizer = ToktokTokenizer()

    # Tokenize the input data using the tokenizer object
    data = tokenizer.tokenize(data, return_str=True)

    # Return the processed data
    return data


def stem(data):
    # Create an instance of the PorterStemmer class from the nltk library
    ps = nltk.porter.PorterStemmer()
    # Create a list of words form data
    words = data.split()
    # Apply stemming to each word in the input data
    stems = [ps.stem(word) for word in words]

    # Join the stemmed words into a single string with spaces in between
    stemmed_data = ' '.join(stems)

    # Return the stemmed data
    return stemmed_data


def lemmatize(data):
    # Create an instance of WordNetLemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Create a list of words form data
    words = data.split()
    
    # Lemmatize each word in the input data
    lemmas = [wnl.lemmatize(word) for word in words]

    # Join the lemmatized words into a single string
    lemmatized_data = ' '.join(lemmas)

    # Return the lemmatized data
    return lemmatized_data

# Function to apply cleaning and processing functions from prepare.py
def process_dataframe(df):
    # Create a new column 'original' and assign the values from 'content'
    df['original'] = df['content']
    
    # Apply the basic_clean function to 'original', then tokenize the result, and remove stopwords
    df['clean'] = df['original'].apply(basic_clean).apply(tokenize).apply(remove_stopwords)
    
    # Apply the stem function to 'clean' column
    df['stemmed'] = df['clean'].apply(stem)
    
    # Apply the lemmatize function to 'clean' column
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    # Drop the 'content' column from the dataframe
    df = df.drop(columns='content', axis=1)
    
    # Return the modified dataframe
    return df


def remove_stopwords(data, extra_words= [], exclude_words= []):
    # Create a list of stopwords in English
    stopwords_list = stopwords.words('english')

    # Extend the stopwords_list with the elements from the extra_words list
    stopwords_list.extend(extra_words)

    # Iterate over each word in the exclude_words list
    for word in exclude_words:
        # Check if the word exists in the stopwords_list
        if word in stopwords_list:
            # Remove the word from the stopwords_list
            stopwords_list.remove(word)

    # Split the data into individual words and filter out stopwords
    words = [word for word in data.split() if word not in stopwords_list]
    
    # Join the filtered words back into a string
    data = ' '.join(words)
    
    # Return the processed data
    return data