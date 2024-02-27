import python_news_scraper

config = {
    "queryVars": "hl=en-US",
    "searchTerm": "python",
}

results = python_news_scraper.googleNewsScraper(config)
print(results[0])