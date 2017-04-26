'''Finds CDNs for the top 1000 Amazon Alexa ranked websites'''

# Standard library imports
import json
from Queue import Empty, Queue
from urlparse import ParseResult, urljoin, urlparse

# Custom library imports
import dns.resolver
import mechanize
from bs4 import BeautifulSoup

# Maximum number of URLs to crawl per page
MAX_URLS = 10


# Get resources for finding CDNs in use
CDN = json.load(open('cdn.json'))


def run():
    '''Run the CDN finder'''
    # Get top URLs
    topurls = [url.strip() for url in list(open('top1000'))]

    # Open browser, make it look real, and make it handle robots/throttling
    browser = mechanize.Browser()
    browser.set_handle_equiv(False)
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; \
                            U; Linux i686; en-US; rv:1.9.0.1) \
                            Gecko/2008071615 Fedora/3.0.1-1.fc9 \
                            Firefox/3.0.1')]


    # Run crawler over CDN
    for url in topurls[199:200]:
        # Open output file
        outfile = open('info/' + url, 'w')

        # Make URL good
        url = urlparse(url, 'http')
        netloc = url.netloc or url.path
        if not netloc.startswith('www.'):
            netloc = 'www.' + netloc
        url = ParseResult('http', netloc, url.path if url.netloc else '',
                          *url[3:]).geturl()

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
            # Get the URL
            try:
                url = queue.get(False)
            except Empty:
                break

            # Get page and parse
            try:
                page = browser.open(url, timeout=15)
            except Exception as exception:
                print exception
                continue
            soup = BeautifulSoup(page.read(), 'lxml')

            # Get same-domain links on the page
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('javascript:'):
                    continue
                if urljoin(url, link['href']) in seenlinks:
                    continue
                if urlparse(link['href']).netloc in [urlparse(url).netloc, '']:
                    seenlinks.add(urljoin(url, link['href']))
                    queue.put(urljoin(url, link['href']))

            # Get diff-domain embedded links
            emblinks = [link['src'] for link in soup.find_all(src=True)]
            emblinks = set([urlparse(emblink).netloc for emblink in emblinks])
            try:
                emblinks.remove('')
            except KeyError:
                pass

            # Get CDN associated with URL
            getcdn(url, page.info(), outfile)

            # For embedded links
            for emblink in emblinks - seenemblinks:
                getcdn('http://' + emblink, {}, outfile)

            # Mark embedded links as done
            seenemblinks = seenemblinks.union(emblinks)

        # Close outfile
        outfile.close()

        # Top URL divider
        print '------------------------------------------------------'

def getcdn(url, headers, outfile):
    '''Get CDN from URL and headers'''
    # Check whether at least one CDN has been written to file
    wrote = False

    # Check headers
    for header in CDN['headers']:
        try:
            if header[1] == headers[header[0]]:
                print url + ',',
                print header[2] + ': Found in headers!'
                outfile.write(url + ',,' + header[2] + ',headers\n')
                wrote = True
        except KeyError:
            pass

    # Check multiheaders
    for hlist in CDN['multiheaders']:
        try:
            if all([header[1] == headers[header[0]] for header in hlist[0]]):
                print url + ',',
                print hlist[1] + ': Found in multiheaders!'
                outfile.write(url + ',,' + hlist[1] + ',multiheaders\n')
                wrote = True
        except KeyError:
            pass

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
