'''Convert out.csv to a LaTeX table'''
from glob import glob
from urlparse import urlparse


def run():
    '''Convert out.csv to a LaTeX table'''
    # Get outcsv, then sort and strip
    outcsv = {entry.split(',')[0]: entry for entry in list(open('out.csv'))}
    categ = 'Top'
    topurls = open('rankings/%s.txt' % categ).read().splitlines()[:250]
    topurls = [urlparse(url).netloc.replace('www.', '') for url in topurls]
    data = [outcsv[entry.strip()].strip() for entry in topurls]

    # Generate LaTeX tables
    with open('table1.tex', 'w') as texfile:
        # Table header
        texfile.write('\\begin{table}[tbp]\n')
        texfile.write('\\centering\n')
        texfile.write('\\caption{Alexa-ranked English websites and their CDNs}\n')
        texfile.write('\\label{cdn-table}\n')
        texfile.write('\\begin{tabular}{|llll|llll|}\n')
        texfile.write('\\hline\n')
        texfile.write('\\# & Domain & 1 & 2 & \\# & Domain & 1 & 2 \\\\\n')
        texfile.write('\\hline\n')

        # Generate entries
        for i in range(70):
            for j in [i, i+70]:
                # Process CSV entry
                url, cdn1, _, cdn2, _, _ = data[j].split(',')
                urlfile = url.replace('.', '_')
                if len(url) > 13:
                    url = url[:10] + '...'
                cdns = [cdn1.replace(' ', '_'), cdn2.replace(' ', '_')]

                # Create rank, icon, URL
                texfile.write(str(j+1) + ' & ')
                texfile.write('\\includegraphics[width=5px]{' +
                              'images/icons/' + urlfile + '.png} ')
                texfile.write(url + ' ')

                # Create CDN icons
                for cdn in cdns:
                    if cdn:
                        texfile.write('& \\includegraphics[width=5px]{' +
                                      'images/cdnicons/' + cdn + '.png} ')
                    else:
                        texfile.write('& ')

                # Insert between columns
                if j == i:
                    texfile.write('& ')

            # Create newline
            texfile.write('\\\\\n')
        texfile.write('\\hline\n')
        texfile.write('\\end{tabular}\n')
        texfile.write('\\end{table}\n\n')

        # Table header
        texfile.write('\\begin{table}[tbp]\n')
        texfile.write('\\centering\n')
        texfile.write('\\begin{tabular}{|llll|llll|}\n')
        texfile.write('\\hline\n')
        texfile.write('\\# & Domain & 1 & 2 & \\# & Domain & 1 & 2 \\\\\n')
        texfile.write('\\hline\n')

        # Generate entries
        for i in range(140, 195):
            for j in [i, i+55]:
                # Process CSV entry
                url, cdn1, _, cdn2, _, _ = data[j].split(',')
                urlfile = url.replace('.', '_')
                if len(url) > 13:
                    url = url[:10] + '...'
                cdns = [cdn1.replace(' ', '_'), cdn2.replace(' ', '_')]

                # Create rank, icon, URL
                texfile.write(str(j+1) + ' & ')
                texfile.write('\\includegraphics[width=5px]{' +
                              'images/icons/' + urlfile + '.png} ')
                texfile.write(url + ' ')

                # Create CDN icons
                for cdn in cdns:
                    if cdn:
                        texfile.write('& \\includegraphics[width=5px]{' +
                                      'images/cdnicons/' + cdn + '.png} ')
                    else:
                        texfile.write('& ')

                # Insert between columns
                if j == i:
                    texfile.write('& ')

            # Create newline
            texfile.write('\\\\\n')
        texfile.write('\\hline\n')
        texfile.write('\\end{tabular}\n')

        # Create legend header
        texfile.write('\\begin{tabular}{|lll|}\n')
        texfile.write('&& \\\\\n')
        texfile.write('\\textbf{CDNs:} && \\\\\n')
        texfile.write('&& \\\\\n')

        # Create legend entries
        cdnicons = glob('cdnicons/*')
        for i, cdnfile in enumerate(cdnicons):
            cdnfile = cdnfile.split('/')[-1].split('.')[0]
            cdn = cdnfile.replace('_', ' ')
            texfile.write('\\includegraphics[width=8px]{images/cdnicons/' +
                          cdnfile + '} ' + cdn)
            newline = (i % 3 == 2) or (i == len(cdnicons)-1)
            if i == len(cdnicons)-1:
                texfile.write(' ' + '&' * (2-(i%3)))
            texfile.write(' \\\\\n' if newline else ' &\n')

        # End table
        texfile.write('&& \\\\\n')
        texfile.write('\\hline\n')
        texfile.write('\\end{tabular}\n')
        texfile.write('\\end{table}\n')

# Run the table generator
if __name__ == "__main__":
    run()
