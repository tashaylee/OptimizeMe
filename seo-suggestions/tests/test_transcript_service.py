import pytest
from pytrends.request import TrendReq
from pathlib import Path



FILE_NAME = Path(__file__).with_name('transcript.txt')
TOP_COUNT = 15
CATEGORY = 'finance'

def test_set_transcript_words(commonly_used_words_from_transcript):
    assert len(commonly_used_words_from_transcript) >= 20

def test_construct_pytrend_youtube_as_gprop(construct_pytrend_youtube_as_gprop):
    assert isinstance(construct_pytrend_youtube_as_gprop, TrendReq)

def test_get_queries_youtube_as_gprop(google_trends_service, commonly_used_words_from_transcript):
    google_trends_service.construct_pytrend(commonly_used_words_from_transcript, CATEGORY)
    queries = google_trends_service.get_queries()
    assert len(queries.keys()) > 0

def test_get_queries_google_search_as_gprop(google_trends_service, commonly_used_words_from_transcript):
    google_trends_service.construct_pytrend(commonly_used_words_from_transcript, CATEGORY, engine='')
    queries = google_trends_service.get_queries()
    assert len(queries.keys()) > 0

def test_keywords_and_queries(youtube_keywords_and_queries, google_search_keywords_and_queries):
    assert 'transcript_keyword' and 'trending_query' in youtube_keywords_and_queries.columns
    assert 'transcript_keyword' and 'trending_query' in google_search_keywords_and_queries.columns