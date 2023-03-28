import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.text import Text 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np

class Transcript():
    def __init__(self, filename):
        self.__filename:str = filename
        self.commonly_used_words = list()

    def common_terms(self) -> list[str]:
        """ Retrieves most common collocations from a text file """
        df = pd.read_csv(self.__filename, sep="delimiter", header=None, engine='python')
        lemmatizer = WordNetLemmatizer()
        ignored_words = stopwords.words("english")
        
        # clean up transcript words and lemmatizes them
        df[0] = df[0].apply(lambda sentence: sentence.lower()).apply(word_tokenize)
        lemmatized_col = df[0].apply(lambda x: [lemmatizer.lemmatize(word) for word in x if word.isalnum() and word not in ignored_words])
        lemmatized_words = np.concatenate(lemmatized_col, axis=0)
    
        terms = Text(lemmatized_words)
        all_terms = [" ".join(term) for term in terms.collocation_list()]

        self.set_commonly_used_words(list_of_terms= all_terms)
    
    def set_commonly_used_words(self, list_of_terms):
        """ Sets all the collocations of words in a transcript"""
        self.commonly_used_words = list_of_terms
        
    def get_commonly_used_words(self) -> list[str]:
        """ Getter for commonly used words in a transcript"""
        return self.commonly_used_words

