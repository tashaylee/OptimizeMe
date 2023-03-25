import pytest
from transcript import Transcript
from service import GoogleTrendsService
from pathlib import Path

FILE_NAME = Path(__file__).with_name('transcript1.txt')
CATEGORY = 'finance'
@pytest.fixture
def transcript():
    return Transcript(FILE_NAME)

@pytest.fixture
def set_transcript(transcript):
    return transcript.common_terms()

@pytest.fixture
def commonly_used_words_from_transcript(transcript, set_transcript):
    commonly_used_words = transcript.get_commonly_used_words()
    return commonly_used_words


@pytest.fixture
def google_trends_service():
    return GoogleTrendsService()

@pytest.fixture
def construct_pytrend(google_trends_service, commonly_used_words_from_transcript):
    return google_trends_service.construct_pytrend(commonly_used_words_from_transcript, category=CATEGORY)

@pytest.fixture
def queries(google_trends_service, construct_pytrend):
    return google_trends_service.get_top_queries()