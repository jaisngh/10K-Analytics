# 10K-Analytics
## Scraping and Textual Analysis of 10K Form Filings
A script for scraping and conducting textual analysis on the "Management's Discussion and Analysis" section of SEC Form 10K filings
**run with *Main.py***<br>
The final analysis is output as csv file in the working directory as ***sec_edgar_completed_analysis.csv***<br>
To add a filing to be analyzed, add the company name under 'Company' and the link to the relevant 10k filing  <br> (can be found at https://www.sec.gov/edgar/search/) under 'Filings URL' to ***sec_src.csv***


## Overview
This script scrapes Form 10-K filings from the SEC Edgar database and parses them to extract *Item 7: Management's Discussion and Analysis of Financial Condition and Results of Operations*. The 10K Filings and URLs from the Edgar database are linked in the sec_src.csv file.

The extracted text is then cleaned by removing any 'stop words' present in the text (the stop words file can be found at https://sraf.nd.edu/textual-analysis/resources/#StopWords) and tokenized<br>
A Textual Analysis is then done on the tokenized cleaned text to calculate 8 variables:

* Word Count: Number of words
* Positivity score: Number of positive words in the text
* Negativity score: Number of negative words in the text
* Polarity score: (Positive Score - Negative Score) / (Positive Score + Negative Score)
* Complex Word Count: Number of words greater than 2 syllables
* Average Sentence Length: The average number of words per sentence
* Percent of Complex Words: Complex Word Count / Word Count
* Gunning Fog Index: 0.4 * (Average Sentence Lenght + 100 * Percent of Complex Words)

Note: 'Positive' and 'negative' words are sourced from the Loughran-McDonald Master Dictionary, available here: https://sraf.nd.edu/textual-analysis/resources/#Master%20Dictionary

## External Libraries and Resources
External packages and libraries used for scraping and analysis are *Pandas*, *nltk*, and *BeautifulSoup*
