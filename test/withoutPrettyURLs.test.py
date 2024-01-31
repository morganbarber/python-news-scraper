import unittest
from expectpy import expect
from index import gns

class TestWithoutPrettyURLs(unittest.TestCase):
  def test_should_have_articles(self):
    articles = gns({
      "searchTerm": "ethereum",
      "queryVars": {
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en"
      },
      "prettyURLs": False,
      "timeframe": "1h",
      "puppeteerArgs": [
        "--no-sandbox",
        "--disable-setuid-sandbox"
      ]
    })
    expect(articles).to_not_be_empty()

if __name__ == "__main__":
  unittest.main()
