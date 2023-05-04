import requests
from bs4 import BeautifulSoup

# Our url to scrape
url = 'http://quotes.toscrape.com/'

# Checking url connection
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, 'lxml')
#print(soup)

# find and print all texts of qoutes on 1 page
qoutes = soup.find_all('span', class_ = 'text')
print(len(qoutes))
print(type(qoutes))
for qoute in qoutes:
    print(qoute.text)

# find all authors and print their names
authors = soup.find_all('small', class_ = 'author')
for author in authors:
    print(author.text)

#
tags = soup.find_all('div', class_ = 'tags')

for i in range(len(qoutes)):
    print(qoutes[i].text)
    print(f'BY {authors[i].text}')
    tags_for_qoute = tags[i].find_all('a', class_ = 'tag')

    for tag_for_qoute in tags_for_qoute:
        print(f'|{tag_for_qoute.text}', end='| ')