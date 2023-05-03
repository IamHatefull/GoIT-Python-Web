import requests
from bs4 import BeautifulSoup

# Our url to scrape
url = 'http://quotes.toscrape.com/'

# Checking url connection
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, 'lxml')
#print(soup)

qoutes = soup.find_all('span')
print(qoutes)