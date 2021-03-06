'''Convert out.csv to a LaTeX table'''
from collections import Counter


def run(categ='Top'):
    '''Convert out.csv to a LaTeX table'''
    # Get outcsv, then sort and strip
    infile = 'out/out_%s.csv' % categ
    outcsv = zip(*[entry.split(',') for entry in list(open(infile))])
    _, cdn1s, _, cdn2s, _, _ = outcsv

    freq = Counter(cdn1s) + Counter(cdn2s)
    del freq['']
    total = float(sum(freq.values()))

    # Generate LaTeX tables
    with open('out/table2.tex', 'w') as texfile:
        # Table header
        texfile.write('\\begin{table}[tbp]\n')
        texfile.write('\\centering\n')
        texfile.write('\\caption{Aggregate Statistics for CDN Usage}\n')
        texfile.write('\\label{cdn-stats-table}\n')
        texfile.write('\\begin{tabular}{|lllll|}\n')
        texfile.write('\\hline\n')
        texfile.write('\\# & CDN & No. Domains & \\% CDN & \\% total \\\\\n')
        texfile.write('\\hline\n')

        # Generate entries
        for i, (cdn, num) in enumerate(freq.most_common()):
            # Process CDN name
            cdnfile = cdn.replace(' ', '_')

            # Create rank, icon, URL
            texfile.write(str(i+1) + ' & ')
            texfile.write('\\includegraphics[width=8px]{' +
                          'images/cdnicons/' + cdnfile + '.png} ')
            texfile.write(cdn + ' & ' + str(num) + ' & ')
            texfile.write('%.1f' % (num/total*100) + '\\% & ')
            texfile.write(str(num/250.*100) + '\\%')

            # Create newline
            texfile.write('\\\\\n')
        texfile.write('\\hline\n')
        texfile.write('\\end{tabular}\n')
        texfile.write('\\end{table}\n\n')


# Run the table generator
if __name__ == "__main__":
    run()
