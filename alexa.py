'''Retrieve Alexa top sites'''

# Standard library imports
import json

# Custom library imports
import awis

# Get Alexa keys
AWS_ACCESS_KEY, AWS_SECRET_KEY = open('alexa_keys.txt').read().splitlines()

CATEGORIES = 'Adult Arts Business Computers Games Health Home Kids_and_Teens \
              News Recreation Reference Regional Science Shopping Society \
              Sports'


def run():
    '''Test the Alexa Python client'''
    api = awis.AwisApi(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    for categ in CATEGORIES.split() + ['']:
        print categ ####
        urls = []
        while len(urls) < 500:
            count = min(500-len(urls), api.MAX_CATEGORY_LISTINGS_COUNT)
            tree = api.category_listings('Top/' + categ if categ else 'Top',
                                         Recursive=True,
                                         SortBy='Popularity',
                                         Count=count,
                                         Start=len(urls)+1,
                                         Descriptions=False)
            new_urls = tree.findall('//{%s}DataUrl' % api.NS_PREFIXES['awis'])
            if len(new_urls) != 0:
                urls += [item.text for item in new_urls]
            else:
                break
        print urls #####
        print len(urls) #####
        if not categ:
            categ = 'Top'
        with open('rankings/' + categ + '.txt', 'w') as outfile:
            outfile.write('\n'.join(urls))


# Run the table generator
if __name__ == '__main__':
    run()
