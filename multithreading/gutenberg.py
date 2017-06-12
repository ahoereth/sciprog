"""
This week we’ll have an exercise about multithreading and some web scraping.
For this you’ll want to install two Python libraries requests and Beautiful
Soup.
Links to documentation:
http://docs.python-requests.org/en/master/
https://www.crummy.com/software/BeautifulSoup/
For this exercise, you’ll use requests to pull data from Project Gutenberg.
Using the top 20 books from the last 30 days, count how many of each vowel
appears in each book separately so the end result is a dictionary of book name
to dictionary of vowel to its count, so basically a dictionary of dictionaries.
You should also try to use multithreading/multiprocessing as seems appropriate
using the concurrent.futures library included with Python.
Make a folder multithreading and a file called gutenberg.py in there. Save
your script in a function called top_20, like the following:
"""

from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


def get_toplist(id):
    r = requests.get('https://www.gutenberg.org/browse/scores/top')
    soup = BeautifulSoup(r.text, 'html.parser')
    lis = soup.find(id=id).find_next_sibling('ol').find_all('li')
    hyperlinks = [li.find('a') for li in lis]
    return [a['href'] for a in hyperlinks]


def get_book(href):
    page = requests.get('https://www.gutenberg.org' + href)
    soup = BeautifulSoup(page.text, 'html.parser')
    link = soup.find(string='Plain Text UTF-8')
    if link is None:
        return None
    title = soup.find('div', {'id': 'content'}) \
        .find('div', {'class': 'header'}) \
        .find('h1') \
        .text
    book = requests.get('https:' + link.parent['href'])
    return title, book.text


def count_vowels(text):
    """Count vowels in text."""
    vowels = 'aeiou'
    return dict(zip(vowels, list(map(text.lower().count, vowels))))


def top_20():
    top20 = get_toplist('books-last30')[:20]

    with ThreadPoolExecutor(max_workers=10) as executor:
        books = executor.map(get_book, top20)

    return dict([(title, count_vowels(text)) for title, text in books])


if __name__ == '__main__':
    from pprint import pprint
    pprint(top_20())
