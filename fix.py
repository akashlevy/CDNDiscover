'''Find CDNs and fix missing CDNs'''
import glob


def find():
    '''Find CDNs and fix missing CDNs'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        # Open file
        with open(filename) as infile:
            # Read each line in the file
            for line in infile.readlines():
                # Split the data
                data = line.strip().split(',')

                # Check if CDN is there
                if data[3] == 'none':
                    if 'cdn' in data[0]:
                        print data[0]
                    if 'cdn' in data[1]:
                        print data[1]


def fix_nones():
    '''Find nones and make them length 4'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        import fileinput
        for line in fileinput.input(filename, inplace=True):
            print line.rstrip().replace(',,none', ',,,none')


def fix_alicdn():
    '''Find alicdn and make it Alibaba'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        import fileinput
        for line in fileinput.input(filename, inplace=True):
            if '.alicdn.' in line:
                print line.rstrip().replace(',none', ',Alibaba')
            else:
                print line.rstrip()


def fix_alicdn2():
    '''Find alicdn and make it Alibaba'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        import fileinput
        for line in fileinput.input(filename, inplace=True):
            print line.rstrip().replace(',,Alibaba', ',Alibaba,cname')


def fix_taobao():
    '''Find Taobao and make it Alibaba'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        import fileinput
        for line in fileinput.input(filename, inplace=True):
            print line.rstrip().replace(',Taobao', ',Alibaba')


def fix_netdna():
    '''Find NetDNA and make it MaxCDN'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        import fileinput
        for line in fileinput.input(filename, inplace=True):
            print line.rstrip().replace(',NetDNA,', ',MaxCDN,')


# Run the fixer
if __name__ == "__main__":
    fix_netdna()
