'''Finds CDNs for the top 500 Amazon Alexa ranked websites'''

# Standard library imports
import json
import time
from Queue import Empty, Queue
from urlparse import urljoin, urlparse

# Custom library imports
import dns.resolver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# Maximum number of URLs to crawl per page
MAX_URLS = 10


# Get resources for finding CDNs in use
CDN = json.load(open('cdn.json'))


def run():
    '''Run the CDN finder'''
    # Get top URLs
    categ = 'Top'
    topurls = open('rankings/%s.txt' % categ).read().splitlines()

    # Iterate through topurls
    for url in topurls:
        getcdn(url, outfile)

def getcdn(url, outfile):
    '''Get CDN from URL and headers'''
    # Check whether at least one CDN has been written to file
    wrote = False

    # Check CNAME
    host = urlparse(url).netloc
    try:
        cname = str(dns.resolver.query(host, 'CNAME')[0])
        print cname,
        for cnamematch in CDN['vendors'].keys():
            if cnamematch in cname:
                print url + ',',
                print CDN['vendors'][cnamematch] + ': Found in CNAME!'
                outfile.write(url + ',' + cname + ',' +
                              CDN['vendors'][cnamematch] + ',cname\n')
                wrote = True
    except (dns.resolver.NoAnswer, dns.resolver.Timeout,
            dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        for cnamematch in CDN['vendors'].keys():
            if cnamematch in url:
                print url + ',',
                print CDN['vendors'][cnamematch] + ': Found in name!'
                outfile.write(url + ',,' + CDN['vendors'][cnamematch] +
                              ',name\n')
                wrote = True

    # Write to file if no CDN found
    if not wrote:
        print url + ',', None
        outfile.write(url + ',,,none\n')


# Run the CDN finder
if __name__ == '__main__':
    run()
