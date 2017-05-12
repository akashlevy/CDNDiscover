'''Compiles the information into a CSV'''
from urlparse import urlparse

# Categories compile results for
CATEGORIES = 'Adult Arts Business Computers Games Health Home Kids_and_Teens \
              News Recreation Reference Regional Science Shopping Society \
              Sports'


def run(categ='Top', num=250):
    '''Compiles the information into a CSV'''
    # Get top URLs
    topurls = open('rankings/%s.txt' % categ).read().splitlines()
    topurls = [urlparse(url).netloc.replace('www.', '') for url in topurls]

    # Open output file
    with open('out/out_%s.csv' % categ, 'w') as outfile:
        # Iterate through files
        for i, url in enumerate(topurls[:num]):
            outfile.write(url + ',')
            filename = 'info/%d-%s.txt' % (i, categ)
            # Open file
            with open(filename) as infile:
                # Keep track of CDN counts
                counts = {}

                # Read each line in the file
                for line in infile.readlines():
                    # Get the CDN and increment
                    cdn = line.strip().split(',')[-2]
                    foundurl = line.strip().split(',')[0]

                    # NetDNA is now MaxCDN
                    if cdn == 'NetDNA':
                        cdn = 'MaxCDN'

                    # Increase count
                    if cdn:
                        if cdn not in counts:
                            counts[cdn] = 0
                        # 5 count if same netloc
                        if url in urlparse(foundurl).netloc:
                            counts[cdn] += 5
                        # 1 count
                        else:
                            counts[cdn] += 1

                # Remove Google/Facebook and CDNs where counts are too low
                for cdn, count in counts.items():
                    if count < 4 or cdn == 'Twitter':
                        del counts[cdn]

                # Get maximum CDN counts
                for cdn, count in sorted(counts.items(), key=lambda x: x[1],
                                         reverse=True)[:2]:
                    outfile.write(cdn + ',' + str(count) + ',')
                for _ in range(2-len(counts)):
                    outfile.write(',,')
                outfile.write('\n')


# Run the CDN finder
if __name__ == '__main__':
    run()
    for cat in CATEGORIES.split():
        run(cat, 25)
