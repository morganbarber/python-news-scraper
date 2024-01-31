import unittest
from expectpy import expect
from index import gns

class TestShouldHavePrettyURLs(unittest.TestCase):
  def test_should_have_pretty_urls(self):
    articles = gns({
      "searchTerm": "dogecoin",
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
    expect("news.google.com/articles").not_to_be_in(articles[0]["link"])

if __name__ == "__main__":
  unittest.main()