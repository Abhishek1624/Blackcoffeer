import requests
from bs4 import BeautifulSoup

class Scrape:

    def scrapeData(id,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html5lib')
        article = soup.find('article')

        titleOfArticle = article.find('h1', attrs={'class': 'entry-title'}).text
        bodyOfArticle = article.find('div', attrs= {'class': 'td-post-content'}).text

        file = open(f"textFiles/{id}.txt","a", encoding='utf-8')
        file.write(titleOfArticle)
        file.write(bodyOfArticle)
        file.close()