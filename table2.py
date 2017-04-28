'''Convert out.csv to a LaTeX table'''
from collections import Counter


def run():
    '''Convert out.csv to a LaTeX table'''
    # Get outcsv, then sort and strip
    _, cdn1s, _, cdn2s, _, _, _ = zip(*[entry.split(',') for entry in list(open('out.csv'))])

    freq = Counter(cdn1s) + Counter(cdn2s)
    del freq['']
    total = float(sum(freq.values()))

    # Generate LaTeX tables
    with open('table2.tex', 'w') as texfile:
        # Table header
        texfile.write('\\begin{table}[]\n')
        texfile.write('\\centering\n')
        texfile.write('\\caption{Aggregate Statistics for CDN Usage}\n')
        texfile.write('\\label{cdn-stats-table}\n')
        texfile.write('\\begin{tabular}{|lllll|}\n')
        texfile.write('\\hline\n')
        texfile.write('\\# & CDN & No. of Domains & \\% CDN & \\% total \\\\\n')
        texfile.write('\\hline\n')

        # Generate entries
        for i, (cdn, num) in enumerate(freq.most_common()):
            # Process CDN name
            cdnfile = cdn.replace(' ', '_')

            # Create rank, icon, URL
            texfile.write(str(i+1) + ' & ')
            texfile.write('\\includegraphics[width=8px]{' + cdnfile + '.png} ')
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
