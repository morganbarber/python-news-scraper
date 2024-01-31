from python_news_scraper import python_news_scraper

config = {
    'queryVars': {
        'hl': 'en-US',
        'gl': 'US',
        'ceid': 'US:en'
    },
    'searchTerm': 'python',
    'timeframe': '7d',
    'prettyURLs': True
}

results = python_news_scraper.google_news_scraper(config)
print(results)