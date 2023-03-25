import pytest
from pytrends.request import TrendReq
from pathlib import Path



FILE_NAME = Path(__file__).with_name('transcript.txt')
TOP_COUNT = 15
CATEGORY = 'finance'

def test_set_transcript_words(commonly_used_words_from_transcript):
    breakpoint()
    assert len(commonly_used_words_from_transcript) >= 20

def test_construct_pytrend(construct_pytrend):
    assert isinstance(construct_pytrend, TrendReq)

def test_get_topics_and_queries(google_trends_service, commonly_used_words_from_transcript):
    google_trends_service.construct_pytrend(commonly_used_words_from_transcript, CATEGORY)
    topics_and_queries = google_trends_service.get_topics_and_queries()
    breakpoint()
    assert len(topics_and_queries['topics']) and len(topics_and_queries['queries']) > 0

def test_get_top_queries(topic_and_query_data):
    assert len(topic_and_query_data) > 1
    
