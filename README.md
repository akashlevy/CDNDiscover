# CDNDiscover
Python/Bash scripts to get the CDNs for the top 250 Alexa websites

## Requirements
- Python 2.7
    * beautifulsoup4
    * dnspython
    * mechanize
    * python-awis
    * selenium
    * urllib
- Mozilla Firefox

## Instructions
- Run alexa.py to get the top websites (overall and in top-level categories)
- Run icons.py to get the icons of the top 250 websites
- Run cdn.py
- Install hosts_adblock.txt into Adblock Plus in the Firefox browser
- This will crawl and get info on the top 250 websites
- Run compile.py to convert the compiled information into a CSV
- Run table1.py and table2.py to get LaTeX tables