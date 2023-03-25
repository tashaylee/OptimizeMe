from transcript import Transcript
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

class GoogleTrendsService():
    def __init__(self):
        self.__topics_and_queries = {
            'topics': list(),
            'queries': list()
        }
    
    def __define_category(self, category:str):
        return category.lower().title()
    
    def __get_google_categories(self, pytrend:TrendReq) -> set:
        primary_google_categories = dict()
        for child in pytrend.categories()['children']:
            if child['name'] not in primary_google_categories:
                primary_google_categories[child['name']] = child['id']
        return primary_google_categories
    
    def __split_to_chunks(self, common_terms:list[str]):
        """ splits list into chunks of 5
        Note: pytrend api can only query 5 keywords at once
        """
        for i in range(0, len(common_terms), 5):
            yield common_terms[i:i+5]
    
    def __add_to_topics_and_queries(self, queries:dict, topics:dict):
        self.__topics_and_queries['queries'].append(queries)
        self.__topics_and_queries['topics'].append(topics)
    
    def get_topics_and_queries(self):
        return self.__topics_and_queries
    
    def construct_pytrend(self, common_terms:list[str], category: str) -> TrendReq:
        # Get related queries associated with transcript words
        headers = {'headers': {'User-Agent': 'pytrends'}}
        pytrend = TrendReq(requests_args = headers)

        # specify category so we can narrow down searches
        category = self.__define_category(category=category)

        if category in self.__get_google_categories(pytrend).keys():
            cat = self.__get_google_categories(pytrend)[category]
        else:
            logging.warn(f'couldnt detect {category} as a registered google category')
            logging.info(f'Defaulting category to All Categories')
            cat = 0

        # split common words into 5 different lists to build payload
        common_terms = list(self.__split_to_chunks(common_terms))
        
        # extract top queries and topics in the past week
        for terms in common_terms:
            pytrend.build_payload(kw_list=terms, timeframe=f'now 7-d', cat=cat, geo='US', gprop='youtube')
            queries = pytrend.related_queries()
            topics = pytrend.related_topics()
            self.__add_to_topics_and_queries(queries=queries, topics=topics)
        return pytrend
    
    def get_top_queries(self) -> pd.DataFrame:
        top_queries = np.zeros(shape=(1, 3))

        for pytrend_type, pytrend_result in self.get_topics_and_queries().items():
            for item in pytrend_result:
                for keyword,result in item.items():
                    # get top related queries
                    if result['top'] is not None:
                        top_df = result['top']
                        # gets where query term is searched more than 50% of time
                        top_40_queries = top_df.loc[top_df['value'] >=50]
                        # extracts query terms
                        query_terms = top_40_queries['query']

                        keyword_array = np.array([keyword]*len(query_terms))
                        pytrend_type_array = np.array([pytrend_type]*len(query_terms))

                        top_queries = np.vstack([top_queries, np.stack((keyword_array, query_terms.to_numpy(), pytrend_type_array), axis=1)])
        
        # remove where all rows are 0
        top_queries = top_queries[~np.all(top_queries == 0, axis=1)]

        # convert top keyword + related queries to dataframe
        return pd.DataFrame(top_queries, columns=['keyword', 'query', 'type'])

