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
#print(len(qoutes))
#print(type(qoutes))
#for qoute in qoutes:
#    print(qoute.text)

# find all authors and print their names on 1 page
authors = soup.find_all('small', class_ = 'author')
#for author in authors:
#    print(author.text)

# find all tag blocks 
tags = soup.find_all('div', class_ = 'tags')

# print qoutes with authors and tags for each qoute.
'''for i in range(len(qoutes)):
    print(qoutes[i].text)
    print(f'BY {authors[i].text}')
    # separating all tags in each block
    tags_for_qoute = tags[i].find_all('a', class_ = 'tag')

    for tag_for_qoute in tags_for_qoute:
        print(f'|{tag_for_qoute.text}', end='| ')
    # Because tags print ends with '| ' we need another print to jump on the next line.
    print('')'''

def qoutes_authors_tags():
    url = 'http://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    qoutes = soup.find_all('span', class_ = 'text')
    authors = soup.find_all('small', class_ = 'author')
    tags = soup.find_all('div', class_ = 'tags')

    for i in range(len(qoutes)):
        print(qoutes[i].text)
        print(f'BY {authors[i].text}')
        tags_for_qoute = tags[i].find_all('a', class_ = 'tag')

        for tag_for_qoute in tags_for_qoute:
            print(f'|{tag_for_qoute.text}', end='| ')
        
        # Because tags print ends with '| ' we need another print to jump on the next line
        #and '\n' to make space between lines to make it more readable
        print('\n')

qoutes_authors_tags()
