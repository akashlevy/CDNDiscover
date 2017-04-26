'''Compiles the information into a CSV'''
import glob

def run():
    '''Compiles the information into a CSV'''
    # Open output file
    with open('out.csv', 'w') as outfile:
        # Iterate through files
        for filename in glob.glob('info/*'):
            url = filename.split('/')[-1]
            outfile.write(url + ',')
            # Open file
            with open(filename) as infile:
                # Keep track of CDN counts
                counts = {}

                # Read each line in the file
                for line in infile.readlines():
                    # Get the CDN
                    cdn = line.strip().split(',')[2]
                    if cdn:
                        try:
                            counts[cdn] += 1
                        except KeyError:
                            counts[cdn] = 1

                # Get maximum CDN counts
                for cdn, count in sorted(counts.items(), key=lambda x: x[1],
                                         reverse=True)[:3]:
                    outfile.write(cdn + ',' + str(count) + ',')
                for _ in range(3-len(counts)):
                    outfile.write(',,')
                outfile.write('\n')


# Run the CDN finder
if __name__ == '__main__':
    run()
