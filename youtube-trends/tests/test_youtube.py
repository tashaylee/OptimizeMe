from youtube import Youtube
import pytest

@pytest.fixture
def youtube():
    return Youtube()

def test_search_associated_terms(youtube, queries):
    youtube.get_trending_video_data(queries)
    breakpoint()