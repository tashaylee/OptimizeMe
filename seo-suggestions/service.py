from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import logging

class GoogleTrendsService():
    def __init__(self):
        self.__queries = dict()
    
    def _define_category(self, category:str):
        return category.lower().title()
    
    def _get_google_categories(self, pytrend:TrendReq) -> set:
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
    
    def set_queries(self, queries_dict):
        self.__queries.update(queries_dict)

    def get_queries(self) -> dict:
        return self.__queries
    
    def construct_pytrend(self, common_terms:list[str], category: str, engine:str='') -> TrendReq:
        # Get related queries associated with transcript words
        headers = {'headers': {'User-Agent': 'pytrends'}}
        pytrend = TrendReq(requests_args = headers)

        # specify category so we can narrow down searches
        category = self._define_category(category=category)

        if category in self._get_google_categories(pytrend).keys():
            cat = self._get_google_categories(pytrend)[category]
        else:
            logging.warn(f'Couldnt detect "{category}" as a registered google category \n\nDefaulting category to All Categories')
            cat = 0

        # split common words into 5 different lists to build payload
        common_terms = list(self.__split_to_chunks(common_terms))
        
        # extract top queries and topics in the past week
        for terms in common_terms:
            pytrend.build_payload(kw_list=terms, timeframe=f'now 7-d', cat=cat, geo='US', gprop=engine)
            pytrend_queries = pytrend.related_queries()
            self.set_queries(queries_dict= pytrend_queries)
        return pytrend
    
    """ Retrieves the top 50% of trending queries.
    Return: Dataframe containing transcript keywords and trending queries related to it. """
    def keywords_and_queries(self) -> pd.DataFrame:
        top_queries = np.zeros(shape=(1, 2))
        for key_term, term_df in self.get_queries().items():
            # Get top queries related to transcript key term
            top_df = term_df['top']
            if top_df is not None:
                # get query terms searched more than 50% of time
                top_50_queries_df = top_df.loc[top_df['value'] >=50]
                related_queries = top_50_queries_df['query']
                
                keyterm_array = np.array([key_term]*len(related_queries))
                top_queries = np.vstack([top_queries, np.stack((keyterm_array, related_queries.to_numpy()), axis=1)])

        # remove where all rows are 0
        top_queries = top_queries[~np.all(top_queries == 0, axis=1)]

        # convert top keyword + related queries to dataframe
        df =  pd.DataFrame(top_queries, columns=['transcript_keyword', 'trending_query'])
        return df
    
    def export_to_csv(self, queries_df:pd.DataFrame):
        queries_df.to_csv("seo_term_suggestions.csv", index=False)
        return