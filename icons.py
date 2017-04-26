'''Gets the icons for the top 500 websites and stores them locally'''

# Custom library imports
from urllib import urlopen


def run():
    '''Run the CDN finder'''
    # Get URLs in top 1000 list
    for url in [url.strip() for url in list(open('top1000'))][:250]:
        icon = urlopen('https://www.google.com/s2/favicons?domain=www.' + url)
        with open('icons/' + url + '.ico', 'wb') as iconfile:
            iconfile.write(icon.read())

# Run the icon getter
if __name__ == '__main__':
    run()
