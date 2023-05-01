import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com/'

response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, 'lxml')

print(soup)