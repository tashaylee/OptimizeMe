from youtube import Youtube
import pytest

@pytest.fixture
def youtube():
    return Youtube()

def test_search_associated_terms(youtube, youtube_keywords_and_queries):
    suggested_youtube_tags = youtube.get_trending_video_data(youtube_keywords_and_queries)
    assert 'tags' in suggested_youtube_tags.columns
    assert suggested_youtube_tags['tags'].size > 0