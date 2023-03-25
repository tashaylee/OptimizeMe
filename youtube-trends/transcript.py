import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.text import Text 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Transcript():
    def __init__(self, filename):
        self.__filename:str = filename
        self.commonly_used_words = list()

    def common_terms(self) -> list[str]:
        import re
        """ Retrieves most common collocations from a text file """
        df = pd.read_csv(self.__filename, sep="delimiter", header=None, engine='python')

        # lemmatizing words reduces words to core meaning
        lemmatizer = WordNetLemmatizer()
        lemmatized_words=list()
        ignored_words = stopwords.words("english")

        df[0] = df[0].apply(lambda x: x.lower()).apply(word_tokenize)
        
        for index, values in df[0].items():
            for word in values:
                if word.isalnum() and word not in ignored_words:
                    lemmatized_words.append(lemmatizer.lemmatize(word))
    
        terms = Text(lemmatized_words)
        all_terms = [" ".join(term) for term in terms.collocation_list()]

        self.commonly_used_words = all_terms
        
    def get_commonly_used_words(self) -> list[str]:
        """ Getter for commonly used words in a transcript"""
        return self.commonly_used_words




