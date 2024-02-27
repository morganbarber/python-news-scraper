from bs4 import BeautifulSoup
from pyppeteer import launch

verifyMessages = [
    "you are human",
    "are you human",
    "i'm not a robot",
    "recaptcha"
]

async def getArticleContent(articles, filterWords):
    try:
        browser = await launch()
        processedArticlesPromises = [extractArticleContentAndFavicon(article, browser, filterWords) for article in articles]
        processedArticles = await asyncio.gather(*processedArticlesPromises)
        await browser.close()
        return processedArticles
    except Exception as err:
        # print("getArticleContent ERROR:", err)
        return articles

async def extractArticleContentAndFavicon(article, browser, filterWords):
    try:
        page = await browser.newPage()
        await page.goto(article['link'], waitUntil='networkidle2')
        content = await page.content()

        favicon = await page.evaluate('''
            () => {
                const link = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');
                return link ? link.getAttribute('href') : '';
            }
        ''')

        soup = BeautifulSoup(content, 'html.parser')
        articleContent = soup.get_text(separator='\n')

        if not articleContent:
            # print("Article content could not be parsed or is empty.")
            return { **article, 'content': '', 'favicon': favicon }

        hasVerifyMessage = any(w in articleContent.lower() for w in verifyMessages)
        if hasVerifyMessage:
            # print("Article requires human verification.")
            return { **article, 'content': '', 'favicon': favicon }

        cleanedText = cleanText(articleContent, filterWords)

        if len(cleanedText.split(' ')) < 100:  # Example threshold: 100 words
            # print("Article content is too short and likely not valuable.")
            return { **article, 'content': '', 'favicon': favicon }

        # print("SUCCESSFULLY SCRAPED ARTICLE CONTENT:", cleanedText)
        return { **article, 'content': cleanedText, 'favicon': favicon }
    except Exception as error:
        # print('Error extracting article with Puppeteer:', error)
        return { **article, 'content': '', 'favicon': '' }

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