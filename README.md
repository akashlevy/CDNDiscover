# CDNDiscover
Python/Bash scripts to get the CDNs for the top 250 Alexa websites

## Requirements
- Python 2.7
- dnspython
- mechanize
- BeautifulSoup4

## Instructions
- Run icons.py to get the icons of the top 250 websites
- Run cdn.py to crawl and get info on the top 250 websites
- Run ignore.py to ignore websites hosting particular static content
- Run compile.py to convert the compiled information into a CSV
- Edit out.csv as necessary
- Run table.py to get LaTeX output
- (The file fix.py was simply to correct some earlier mistakes made)