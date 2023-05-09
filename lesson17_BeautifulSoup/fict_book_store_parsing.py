import requests
from bs4 import BeautifulSoup

# url to scrape
url = 'http://books.toscrape.com/'

# Cheking response status code. If '200', then we're connected.
response = requests.get(url)
print(response.status_code)

# Read page from url
soup = BeautifulSoup(response.text, 'lxml')
#print(soup)

books = soup.find_all('article', class_ = 'product_pod')

titles = soup.find_all('h3')

# Print titles of the books
for title in titles:
    name = title.find('a').attrs['title']
    print(name)