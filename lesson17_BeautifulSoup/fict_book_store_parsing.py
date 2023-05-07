import requests
from bs4 import BeautifulSoup


url = 'http://books.toscrape.com/'

response = requests.get(url)
print(response.status_code)

soup = BeautifulSoup(response.text, 'lxml')
#print(soup)

books = soup.find_all('article', class_ = 'product_pod')

titles = soup.find_all('a', class_ = 'title')
print(titles)