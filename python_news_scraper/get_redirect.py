# get redirect of url

import requests
from bs4 import BeautifulSoup

def get_redirect(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    redirect = response.url
    return redirect
