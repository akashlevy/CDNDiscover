'''Ignores sites in the ignorelist'''
import glob


def ignoresites():
    '''Find bad sites and remove'''
    # Iterate through files
    for filename in glob.glob('info/*'):
        import fileinput
        for line in fileinput.input(filename, inplace=True):
            ignorelist = [url.strip() for url in list(open('ignorelist'))]
            if not any([ignored in line for ignored in ignorelist]):
                print line.rstrip()


# Run the fixer
if __name__ == "__main__":
    ignoresites()
