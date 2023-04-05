from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
load_dotenv('.env')
from optimizeme.utils import download_nltk
download_nltk()
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser

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
        req = self.youtube.videos().list(id=video_id, maxResults=1, part="snippet, status, statistics").execute()
        return req.get("items", None)

    
    def get_trending_video_data(self, top_queries:pd.DataFrame):
        all_trending = np.zeros(shape=(1, 3))
        queries = top_queries['trending_query']

        # find the videos that rank for trending top_queries
        for query in queries:
            video_result_for_query = self.__search_videos_response(query=query, max_result=5)
            for video_result in video_result_for_query:

                # skip evaluating more videos if we already have atleast 3 videos tags
                if all_trending[:, 1].tolist().count(query) >= 3:
                    break
                
                # extract video data from trending videos associated with query
                video_id = video_result.get('id', None).get('videoId', None)
                video = self.__video_resource_response(video_id=video_id)[0]
                tags = video.get('snippet').get('tags', None)
                published_at = video.get('snippet').get('publishedAt')
                like_count = video.get('statistics').get('likeCount', None)
                view_count = video.get('statistics').get('viewCount', None)
                transcript_keyword = top_queries.loc[top_queries['trending_query'] == query].iloc[0]['transcript_keyword']
                
                if tags is None:
                    continue

                # Only evaluate videos that are at least 2 years old
                published_at = parser.parse(published_at)
                now = datetime.now()
                two_years_ago = now - relativedelta(years=2)

                if not published_at.date() >= two_years_ago.date():
                    continue
                
                # create a new row for video data + suggested terms
                try:
                    # only create row if video has high likes/views
                    if (len(like_count) and len(view_count)) >= 5:
                        channel_info = np.array([[transcript_keyword, query, tags]], dtype=object)
                        all_trending = np.vstack([all_trending, channel_info])
                except TypeError as e:
                    logging.warning(f"Missing like or view count for video.")
                    continue
                
        # remove where all rows are 0
        all_trending = np.delete(all_trending, (0), axis=0)
        
        df = pd.DataFrame(all_trending, columns=["transcript_keyword", "query_term", "tags"])
        return df

        