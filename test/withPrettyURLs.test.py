import unittest
from expectpy import expect
from index import gns

class TestWithPrettyURLs(unittest.TestCase):
  def test_should_have_articles_with_prettyURLs(self):
    articles = gns({
      "searchTerm": "bitcoin",
      "queryVars": {
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en"
      },
      "prettyURLs": True,
      "timeframe": "1h",
      "puppeteerArgs": [
        "--no-sandbox",
        "--disable-setuid-sandbox"
      ]
    })
    expect(articles).to_not_be_empty()

if __name__ == "__main__":
  unittest.main()
