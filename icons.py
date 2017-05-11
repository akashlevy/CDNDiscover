'''Gets the icons for the top 500 websites and stores them locally'''

# Custom library imports
from urllib import urlopen
from urlparse import urlparse


def run():
    '''Run the CDN finder'''
    # Get URLs in top 1000 list
    cat = 'Top'
    for url in open('rankings/%s.txt' % cat).read().splitlines()[:250]:
        icon = urlopen('https://www.google.com/s2/favicons?domain=' + url)
        netloc = urlparse(url).netloc.replace('www.', '')
        with open('icons/%s.png' % netloc.replace('.', '_'), 'wb') as iconfile:
            iconfile.write(icon.read())

# Run the icon getter
if __name__ == '__main__':
    run()
