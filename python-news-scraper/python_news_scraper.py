import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import datetime

def google_news_scraper(config):
    query_vars = config.get('queryVars', {})
    query_string = urlencode(query_vars)
    search_term = config.get('searchTerm', '')
    timeframe = config.get('timeframe', '7d')
    url = f'https://news.google.com/search?{query_string}&q={search_term}+when:{timeframe}'
    print(f'SCRAPING NEWS FROM: {url}')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }

    cookies = {
        'CONSENT': f'YES+cb.{datetime.date.today().strftime("%Y%m%d")}-04-p0.en-GB+FX+667'
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    articles = soup.find_all('article')
    results = []

    for article in articles:
        link = article.find('a', href=True)
        if link and link['href'].startswith('./article'):
            link = f'https://news.google.com/{link["href"].replace("./", "")}'
        else:
            link = None

        image = article.find('figure').find('img')
        if image:
            srcset = image.get('srcset')
            if srcset:
                srcset = srcset.split(' ')
                image = srcset[-2] if srcset else None
            else:
                image = image.get('src')
        else:
            image = None

        main_article = {
            'title': article.find('h4').text or article.find('div > div + div > div a').text,
            'link': link,
            'image': f'https://news.google.com{image}' if image and image.startswith('/') else image,
            'source': article.find('div', {'data-n-tid': True}).text or None,
            'datetime': datetime.datetime.strptime(article.find('div:last-child time')['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ') if article.find('div:last-child time') else None,
            'time': article.find('div:last-child time').text or None
        }

        results.append(main_article)

    if config.get('prettyURLs'):
        for article in results:
            response = requests.get(article['link'])
            data = response.content
            soup = BeautifulSoup(data, 'html.parser')
            link = soup.find('c-wiz', {'a': {'rel': 'nofollow'}})
            if link:
                article['link'] = link.get('href')

    return [result for result in results if result['title']]
