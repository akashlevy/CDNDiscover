'''Compiles the information into a CSV for making radar plot'''

# Standard library imports
import json
from collections import Counter


# Categories compile results for
CATEGORIES = 'Adult Arts Business Computers Games Health Home Kids_and_Teens \
              News Recreation Reference Regional Science Shopping Society \
              Sports'

# Get resources for finding CDNs in use
#CDNS = sorted(set(json.load(open('cdn.json'))['vendors'].values()))
CDNS = ['Akamai', 'Amazon CloudFront', 'Cloudflare', 'Fastly', 'Highwinds',
        'Incapsula', 'Instart Logic']


def run():
    '''Compiles the information into a CSV for making radar plot'''
    # Open outfile
    outfile = open('out/radar.csv', 'w')

    # Write header
    outfile.write(',%s\n' % ','.join(CDNS))

    # Iterate over categories
    for categ in CATEGORIES.split():
        # Get CDNs in category
        infile = 'out/out_%s.csv' % categ
        outcsv = zip(*[entry.split(',') for entry in list(open(infile))])
        _, cdn1s, _, cdn2s, _, _ = outcsv

        # Get frequency of CDNs
        freq = Counter(cdn1s) + Counter(cdn2s)
        del freq['']

        # Write line out to file
        cdnfreq = []
        for cdn in CDNS:
            try:
                cdnfreq.append(str(freq[cdn]))
            except KeyError:
                cdnfreq.append('0')
        outfile.write('%s,%s\n' % (categ.replace('_', ' '), ','.join(cdnfreq)))

    # Close outfile
    outfile.close()


# Run the main method
if __name__ == '__main__':
    run()
