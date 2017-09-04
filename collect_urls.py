'''Finds CDNs for the top 500 Amazon Alexa ranked websites'''

# Standard library imports
import json

# Custom library imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


# Get resources for finding CDNs in use
CDN = json.load(open('cdn.json'))


def get_browser():
    '''Create the Firefox browser object with Selenium'''
    fprof = webdriver.FirefoxProfile()
    fprof.set_preference("http.response.timeout", 60)
    fprof.set_preference("dom.max_script_run_time", 60)
    browser = webdriver.Firefox(firefox_profile=fprof)
    browser.set_page_load_timeout(100)
    return browser


def run(categ='Top'):
    '''Run the CDN finder'''
    # Get top URLs
    topurls = open('rankings/%s.txt' % categ).read().splitlines()

    # Open browser, make it look real, and make it handle robots/throttling
    browser = get_browser()

    # Run crawler over CDN
    for i, url in enumerate(topurls):
        # Open output file
        outfile = open('info/%d-%s.txt' % (i, categ), 'w')

        # Display original URL name
        print 'THE URL: ' + url

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

        # Extract links to content
        emblinks = set([link['src'] for link in soup.find_all(src=True)])
        try:
            emblinks.remove('')
        except KeyError:
            pass

        # Write extracted links to file
        for emblink in emblinks:
            outfile.write("%s\n" % emblink)
            print emblink

        # Close outfile
        outfile.close()

        # Top URL divider
        print '------------------------------------------------------'


# Run the CDN finder
if __name__ == '__main__':
    run()
