'''Retrieve Alexa top sites'''

# Custom library imports
import awis

# Get Alexa keys
AWS_ACCESS_KEY, AWS_SECRET_KEY = open('alexa_keys.txt').read().splitlines()

# Categories to get top websites for
CATEGORIES = 'Adult Arts Business Computers Games Health Home Kids_and_Teens \
              News Recreation Reference Regional Science Shopping Society \
              Sports'


def run():
    '''Test the Alexa Python client'''
    # Open AWIS API
    api = awis.AwisApi(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Go through categories and request top 500
    for categ in CATEGORIES.split() + ['']:
        # Print category
        print categ

        # Get URLs until there are 500
        urls = []
        while len(urls) < 500:
            # Get as many category listings as possible (up to 500)
            count = min(500-len(urls), api.MAX_CATEGORY_LISTINGS_COUNT)
            tree = api.category_listings('Top/' + categ if categ else 'Top',
                                         Recursive=True,
                                         SortBy='Popularity',
                                         Count=count,
                                         Start=len(urls)+1,
                                         Descriptions=False)

            # Extract URLs of websites and add to list
            new_urls = tree.findall('//{%s}DataUrl' % api.NS_PREFIXES['awis'])
            urls += [item.text for item in new_urls]

        # Print the URLs extracted and how many were extracted (should be 500)
        print urls
        print len(urls)

        # If no category, get general top
        if not categ:
            categ = 'Top'

        # Write rankings out to file
        with open('rankings/' + categ + '.txt', 'w') as outfile:
            outfile.write('\n'.join(urls))


# Run the table generator
if __name__ == '__main__':
    run()
