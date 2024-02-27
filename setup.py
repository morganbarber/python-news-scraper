from setuptools import setup, find_packages

setup(
    name='python-news-scraper',
    version='0.1.0',
    url='https://github.com/morganbarber/python-news-scraper',
    author='Morgan Barber',
    author_email='morganbarber928@gmail.com',
    description='A python package to scrape news.',
    packages=find_packages(),    
    install_requires=['requests', 'beautifulsoup4', 'pyppeteer'],
)