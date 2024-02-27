from bs4 import BeautifulSoup
import requests

verifyMessages = [
    "you are human",
    "are you human",
    "i'm not a robot",
    "recaptcha"
]

def getArticleContent(articles, filterWords):
    processedArticles = []
    for article in articles:
        processedArticle = extractArticleContentAndFavicon(article, filterWords)
        processedArticles.append(processedArticle)
    return processedArticles

def extractArticleContentAndFavicon(article, filterWords):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
    }
    try:
        response = requests.get(article['url'], headers=headers, timeout=1)
        if response.status_code == 200:
            print("response success")
            content = response.text

            favicon = extractFavicon(content)

            soup = BeautifulSoup(content, 'html.parser')
            articleContent = soup.get_text(separator='\n')

            if not articleContent:
                return { **article, 'content': '', 'favicon': favicon }

            hasVerifyMessage = any(w in articleContent.lower() for w in verifyMessages)
            if hasVerifyMessage:
                return { **article, 'content': '', 'favicon': favicon }

            cleanedText = cleanText(articleContent, filterWords)

            if len(cleanedText.split(' ')) < 100:  # Example threshold: 100 words
                return { **article, 'content': '', 'favicon': favicon }

            return { **article, 'content': cleanedText, 'favicon': favicon }
        else:
            print("Response fail")
            return { **article, 'content': '', 'favicon': '' }
    except Exception as error:
        return { **article, 'content': '', 'favicon': '' }

def extractFavicon(content):
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find('link', rel=['icon', 'shortcut icon'])
    return link['href'] if link else ''

def cleanText(text, filterWords):
    unwantedKeywords = [
        "subscribe now",
        "sign up",
        "newsletter",
        "subscribe now",
        "sign up for our newsletter",
        "exclusive offer",
        "limited time offer",
        "free trial",
        "download now",
        "join now",
        "register today",
        "special promotion",
        "promotional offer",
        "discount code",
        "early access",
        "sneak peek",
        "save now",
        "don't miss out",
        "act now",
        "last chance",
        "expires soon",
        "giveaway",
        "free access",
        "premium access",
        "unlock full access",
        "buy now",
        "learn more",
        "click here",
        "follow us on",
        "share this article",
        "connect with us",
        "advertisement",
        "sponsored content",
        "partner content",
        "affiliate links",
        "click here",
        "for more information",
        "you may also like",
        "we think you'll like",
        "from our network",
        *filterWords
    ]
    return '\n'.join(
        line for line in map(str.strip, text.split('\n'))
        if len(line.split(' ')) > 4 and not any(keyword in line.lower() for keyword in unwantedKeywords)
    )