'''Convert out.csv to a LaTeX table'''
import glob


def run():
    '''Convert out.csv to a LaTeX table'''
    # Get outcsv, then sort and strip
    outcsv = {entry.split(',')[0]: entry for entry in list(open('out.csv'))}
    top250 = list(open('top1000'))[:250]
    data = [outcsv[entry.strip()].strip() for entry in top250]

    # Generate LaTeX tables
    with open('table.tex', 'w') as texfile:
        # Table header
        texfile.write('\\begin{table}[]\n')
        texfile.write('\\centering\n')
        texfile.write('\\caption{Alexa-ranked websites and their CDNs}\n')
        texfile.write('\\label{cdn-table}\n')
        texfile.write('\\begin{tabular}{|llll|llll|}\n')
        texfile.write('\\hline\n')
        texfile.write('\\# & Domain & 1 & 2 & \\# & Domain & 1 & 2 \\\\\n')
        texfile.write('\\hline\n')

        # Generate entries
        for i in range(70):
            for j in [i, i+70]:
                # Process CSV entry
                url, cdn1, _, cdn2, _, _, _ = data[j].split(',')
                urlfile = url.replace('.', '_')
                if len(url) > 13:
                    url = url[:10] + '...'
                cdns = [cdn1.replace(' ', '_'), cdn2.replace(' ', '_')]

                # Create rank, icon, URL
                texfile.write(str(j+1) + ' & ')
                texfile.write('\\includegraphics[width=5px]{' + urlfile +
                              '.png} ')
                texfile.write(url + ' ')

                # Create CDN icons
                for cdn in cdns:
                    if cdn:
                        texfile.write('& \\includegraphics[width=5px]{' +
                                      cdn + '.png} ')
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
        texfile.write('\\begin{table}[]\n')
        texfile.write('\\centering\n')
        texfile.write('\\begin{tabular}{|llll|llll|}\n')
        texfile.write('\\hline\n')
        texfile.write('\\# & Domain & 1 & 2 & \\# & Domain & 1 & 2 \\\\\n')
        texfile.write('\\hline\n')

        # Generate entries
        for i in range(140, 195):
            for j in [i, i+55]:
                # Process CSV entry
                url, cdn1, _, cdn2, _, _, _ = data[j].split(',')
                urlfile = url.replace('.', '_')
                if len(url) > 13:
                    url = url[:10] + '...'
                cdns = [cdn1.replace(' ', '_'), cdn2.replace(' ', '_')]

                # Create rank, icon, URL
                texfile.write(str(j+1) + ' & ')
                texfile.write('\\includegraphics[width=5px]{' + urlfile +
                              '.png} ')
                texfile.write(url + ' ')

                # Create CDN icons
                for cdn in cdns:
                    if cdn:
                        texfile.write('& \\includegraphics[width=5px]{' +
                                      cdn + '.png} ')
                    else:
                        texfile.write('& ')

                # Insert between columns
                if j == i:
                    texfile.write('& ')

            # Create newline
            texfile.write('\\\\\n')
        texfile.write('\\hline\n')
        texfile.write('\\end{tabular}\n')

        # Create legend
        for cdnfile in glob.glob('cdnicons/*'):
            cdnfile = cdnfile.split('/')[-1]
            cdn = cdnfile.split('.')[0]
            cdnfile = cdnfile.replace(' ', '_')
            texfile.write('\\includegraphics[width=8px]{' + cdnfile + '} ')
            texfile.write(cdn + ' \\hspace{10mm}\n')


        # End table
        texfile.write('\\hline\n')
        texfile.write('\\end{table}\n')

# Run the table generator
if __name__ == "__main__":
    run()
