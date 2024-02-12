import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class LinkFounder:
    def __init__(self):
        os.mkdir(os.path.dirname(__file__) + '/pages')

    def load_pages(self):
        page = urllib.request.urlopen('https://www.sports.ru/soccer/news/')
        soup = BeautifulSoup(page, 'html.parser')
        links = []
        for link in soup.findAll('a', {'class': 'short-text'}, href=True):
            if link.get('href')[0] == '/':
                link = urllib.parse.urljoin('https://www.sports.ru', link.get('href'))
                links.append(link)
        return links

    def filter_text(self, url):
        request = requests.get(url)
        request.encoding = request.apparent_encoding
        if request.status_code == 200:
            soup = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
            bad_tags = ['style', 'link', 'script']
            for tag in soup.find_all(bad_tags):
                tag.extract()
            return str(soup)
        return None

    def get_links(self, count: int):
        links = list(set(self.load_pages()))
        index_file = open(os.path.dirname(__file__) + '/index.txt', 'w', encoding='utf-8')
        i = 1
        for link in links:
            if i <= count:
                text = self.filter_text(link)
                if text is None:
                    continue
                else:
                    page_name = os.path.dirname(__file__) + '/pages' + '/выкачка' + str(i) + '.html'
                    page = open(page_name, 'w', encoding='utf-8')
                    page.write(text)
                    page.close()
                    index_file.write(str(i) + ' ' + link + '\n')
                    i += 1
            else:
                break
        index_file.close()


if __name__ == '__main__':
    founder = LinkFounder()
    founder.get_links(100)
