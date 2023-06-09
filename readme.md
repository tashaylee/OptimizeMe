# About OptimizeMe
The purpose of this project is to suggest queries that can be used for SEO efforts. Given a transcript or text file, this tool can analyze commonly used terms in your text file, and return related queries from Google or Youtube, which is meant to be used for SEO purposes. 

## How It Works
OptimizeMe is a command line tool. Please download the necessary dependencies before attempting to run it: 
`pip install -r requirements.txt`

One downloaded, you can run:
`cd optimizeme && python main.py`

From there, you can follow the command line prompts, and the output will return in the `seo_term_suggestions.csv` file name.

### Notes
Please add your own `YOUTUBE_API_KEY` as an env var to your .env file. For more notes on how to get your own api key from youtube, <a href="https://developers.google.com/youtube/registering_an_application" target="_blank">visit the Youtube Data API documentation.</a>
