from cgitb import text
import string
import requests
from bs4 import BeautifulSoup

from main import remove_space

class Booksearch():
    def __init__(self, title, comp):
        self.title = title
        self.company = comp
        # self.author = author
        self.price = '0'
        self.status = 'not_found'
    
    def remove_space(self, key):
        return key.replace(' ', '')
    
    def search_url(self, url):
        url = url + self.title
        res = requests.get(url)
        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find('div', attrs={'id' : 'Search3_Result'})
            if results is None:
                return None
            # 검색 결과
            books = results.find_all('div', attrs={'class' : 'ss_book_box'}) 
            if books is None:
                return None
            
            for book in books: # 여러권 검색
                if self.status is 'found':
                    break
                # 책 제목이 같은게 있으면
                ul = book.find('div', attrs={'class' : 'ss_book_list'}).find('ul')
                book_title = ul.find('a', attrs={'class' : 'bo3'})
                if book_title is None:
                   continue
                book_title = self.remove_space(book_title.get_text())
                if book_title != remove_space(self.title):
                    continue
                self.status = 'found'
                # 지은이, 가격, 재고 검색
                li_num = len(ul.find_all('li'))
                li = ul.find('li')
                print(li.find_next_sibling('li').get_text())
                

                