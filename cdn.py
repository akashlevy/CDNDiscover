'''Finds CDNs for the top 500 Amazon Alexa ranked websites'''

# Standard library imports
import glob
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

    # Open browser, make it look real, and make it handle robots/throttling
    fprof = webdriver.FirefoxProfile()
    fprof.set_preference("http.response.timeout", 20)
    fprof.set_preference("dom.max_script_run_time", 15)
    fprof.add_extension(extension='adblock.xpi')
    browser = webdriver.Firefox(firefox_profile=fprof)
    browser.set_page_load_timeout(30)

    # Wait for one minute to load Adblock Plus settings
    time.sleep(60)

    # Run crawler over CDN
    for i, url in enumerate(topurls[:250]):
        # Open output file
        outfile = open('info/%d-%s.txt' % (i, categ), 'w')

        # First item is top domain
        queue = Queue()
        queue.put(url)

        # Links that have already been visited
        seenlinks = set()
        seenemblinks = set()

        # Display original URL name
        print 'THE URL: ' + url

        # Now crawl inner links
        for _ in range(MAX_URLS):
            # Get the URL (if any left)
            try:
                url = queue.get(False)
            except Empty:
                break

            # Get CDN associated with URL
            getcdn(url, outfile)

            # Get page and parse
            try:
                browser.get(url)
                soup = BeautifulSoup(browser.page_source, 'lxml')
            except TimeoutException:
                print 'Loading took too much time!'
                continue
            except Exception as exception:
                print exception
                continue

            # Get same-domain links on the page
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('javascript:'):
                    continue
                if urljoin(url, link['href']) in seenlinks:
                    continue
                if urlparse(link['href']).netloc in [urlparse(url).netloc, '']:
                    seenlinks.add(urljoin(url, link['href']))
                    queue.put(urljoin(url, link['href']))

            # Get diff-domain embedded links that are not scripts/noscripts
            for subtree in soup.findAll(['script', 'noscript']):
                subtree.extract()
            emblinks = [link['src'] for link in soup.find_all(src=True)]
            emblinks = set([urlparse(emblink).netloc for emblink in emblinks])
            try:
                emblinks.remove('')
            except KeyError:
                pass

            # For embedded links
            for emblink in emblinks - seenemblinks:
                getcdn('http://' + emblink, outfile)

            # Mark embedded links as done
            seenemblinks = seenemblinks.union(emblinks)

        # Close outfile
        outfile.close()

        # Top URL divider
        print '------------------------------------------------------'

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
        outfile.write(url.encode('ascii', 'ignore').decode('ascii'))
        try:
            outfile.write(',%s,,none\n' % cname)
        except UnboundLocalError:
            outfile.write(',,,none\n')


def reprocess():
    '''Update all files' hosts: first copy info/ to info.1/, then run'''
    # Get each file in backup folder
    for infile in glob.glob('info.1/*'):
        # Get filename in good folder
        outfile = open(infile.replace('info.1/', 'info/'), 'w')

        # For each line in file, reprocess and put in good file
        for line in open(infile).read().splitlines():
            url = line.split(',')[0].strip()
            getcdn(url, outfile)

        # Close outfile
        outfile.close()


# Run the CDN finder
if __name__ == '__main__':
    run()
