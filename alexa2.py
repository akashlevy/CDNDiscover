'''Retrieve Alexa top sites'''

# Standard library imports
import json

# Custom library imports
import awis

# Get Alexa keys
AWS_ACCESS_KEY, AWS_SECRET_KEY = open("alexa_keys.txt").read().splitlines()


def run():
    '''Test the Alexa Python client'''
    api = awis.AwisApi(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    urls = []
    while len(urls) < 500:
        count = min(500-len(urls), api.MAX_CATEGORY_LISTINGS_COUNT)
        tree = api.category_listings("Top/Adult",
                                     Recursive=True,
                                     SortBy="Popularity",
                                     Count=count,
                                     Start=len(urls)+1,
                                     Descriptions=False)
        new_urls = tree.findall("//{%s}DataUrl" % api.NS_PREFIXES["awis"])
        if len(new_urls) != 0:
            urls += [item.text for item in new_urls]
        else:
            break
    json.dump(urls, open('alexa_global_500.json', 'w'))


# Run the table generator
if __name__ == "__main__":
    run()
