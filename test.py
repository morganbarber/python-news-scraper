import python_news_scraper

config = {
    "queryVars": "hl=en-US",
    "searchTerm": "python",
    "getArticleContent": True,
}

results = python_news_scraper.googleNewsScraper(config)
print(results)
