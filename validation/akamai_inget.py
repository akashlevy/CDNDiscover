'''Finds websites that Akamai hosts from the CSV of extracted links from list
   on their website'''

# Standard library imports
from urlparse import urljoin

# Custom library imports
import pandas as pd
import requests
from bs4 import BeautifulSoup

def run():
    '''Get the links and put them in akamai_in.txt'''
    # Get URLs
    csv = pd.read_csv('validation/akamai_linklist.csv')
    urls = [urljoin('https://www.akamai.com/', url) for url in csv['URL']]

    # For each URL, extract link we want and put it in akamai_in.txt
    with open('validation/akamai_in.txt', 'w') as outfile:
        for url in urls:
            soup = BeautifulSoup(requests.get(url).text, "lxml")
            outfile.write(soup.find('div', class_='sidebarCallout-0').a['href'])
            outfile.write('\n')

if __name__ == '__main__':
    run()
