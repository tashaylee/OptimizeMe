from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
load_dotenv('.env')
from utils import download_nltk
download_nltk()
from nltk.stem import WordNetLemmatizer
from nltk.text import Text
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

API_KEY = os.environ.get('YOUTUBE_API_KEY')

YOUTUBE_SERVICE= "youtube"
API_VERSION = "v3"


class Youtube():
    def __init__(self):
        self.youtube = build(serviceName= YOUTUBE_SERVICE, version= API_VERSION, developerKey = API_KEY)
        self.results:dict = dict()
    
    def __search_videos_response(self, query:str, max_result=10):
        req = self.youtube.search().list(q=query, type="video", maxResults=max_result, part="id").execute()
        return req.get("items", None)
    
    def __video_resource_response(self, video_id:str):
        req = self.youtube.videos().list(id=video_id, maxResults=1, part="snippet").execute()
        return req.get("items", None)

    
    def get_trending_video_data(self, top_queries:pd.DataFrame):
        all_trending = np.zeros(shape=(1, 3))
        queries = top_queries['query']

        # find the videos that rank for trending top_queries
        for query in queries:
            video_result_for_query = self.__search_videos_response(query=query, max_result=3)
            for video_result in video_result_for_query:
                
                # extract video data from trending videos associated with query
                video_id = video_result.get('id', None).get('videoId', None)
                video = self.__video_resource_response(video_id=video_id)[0]
                video_snippet = video.get('snippet')

                title = video_snippet.get('title', None)
                description = video_snippet.get('description', None)
                if description:
                    description = description.split('\n\n')

                # extract the base terms from description text    
                # lemmatizer = WordNetLemmatizer()
                # lemmatized_words = set()

                # df = pd.DataFrame(np.array(description), columns=["description"])
                # df["tokenized_words"] = df["description"].str.casefold().apply(word_tokenize)
                # ignored_words = stopwords.words("english")
                # from nltk.collocations import *
                # finder = BigramCollocationFinder.from_words()

                # for row in df['tokenized_words']:
                #     for word in row:
                #         if word.isalnum():
                #             lw.append(lemmatizer.lemmatize(word))



                # for desc in description:
                #     tokenized_words = word_tokenize(desc.casefold())
                #     for word in tokenized_words:
                #         if word.isalnum():
                #             word = lemmatizer.lemmatize(word)
                #             lemmatized_words.append(word)
                
                # retrieves commonly used pairing of words from description text
                # lemmatized_text= Text(lemmatized_words)
                # suggested_terms = [" ".join(term) for term in lemmatized_text.collocation_list(num=5, window_size=4)]
                
                # create a new row for video data + suggested terms
                channel_info = np.array([[query, video_id, title]], dtype=object)
                all_trending = np.vstack([all_trending, channel_info])
            # remove where all rows are 0
            all_trending = np.delete(all_trending, (0), axis=0)
        
        df = pd.DataFrame(all_trending, columns=["query_term", "video_id", "title"])
        
        breakpoint()


        return pd.DataFrame(all_trending, columns=["query_term", "video_id", "title"])
    
    def lemmatize_title(self, title):
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in title.lower().split(" ")]
        pairs = [" ".join(pair) for pair in nltk.bigrams(lemmatized_words)]
        all_nouns = [pairing[0] for pairing in nltk.pos_tag(pairs) if pairing[1] == "NN" or "NNS"]
    
    def lemmatize_description(self, description):
        pass

        