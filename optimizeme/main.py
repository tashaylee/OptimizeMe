from optimizeme.transcript import Transcript
from optimizeme.service import GoogleTrendsService
from optimizeme.youtube import Youtube

# TO DO:
def main():
    text_path = input("Enter the path to your text file: ")
    category = input("Enter a specific google trends category if known. Otherwise, hit enter: ")
    youtube_search = input(f"Would you like to optimize for youtube search? Enter yes or no: ").lower()
    # Instantiate transcript
    transcript = Transcript(text_path)
    transcript.common_terms()
    commonly_used_words = transcript.get_commonly_used_words()

    service = GoogleTrendsService()
    if youtube_search == "yes":
        engine = 'youtube'
        service.construct_pytrend(commonly_used_words, category=category, engine=engine)
    service.construct_pytrend(commonly_used_words, category=category)
    trending_keywords_and_queries = service.keywords_and_queries()

    if engine == 'youtube':
        suggested_youtube_tags = Youtube().get_trending_video_data(trending_keywords_and_queries)
        service.export_to_csv(suggested_youtube_tags)
    else:
        service.export_to_csv(trending_keywords_and_queries)

if __name__ == '__main__':
    main()
