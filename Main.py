import requests
import time
import re
import os
import pandas as pd
from bs4 import BeautifulSoup
from Analysis import Section

df = pd.read_csv("sec_src.csv", index_col ="Filings URL")
SEC_URL = "https://www.sec.gov/Archives/"



def parse(file):
    soup = BeautifulSoup(file, 'html.parser')
    document_tags = soup.find_all('document')
    for filing_document in document_tags:
        document_type = filing_document.type.find(text=True, recursive=False).strip()
        print(document_type)
        if document_type == "10-K/A" or document_type == "10-K":
            text = filing_document.find('text').extract().text
            matches = re.compile(r'(item\s(7[\.\s]|8[\.\s])|'
                             r'discussion\sand\sanalysis\sof\s(consolidated\sfinancial|financial)\scondition|'
                             r'(consolidated\sfinancial|financial)\sstatements\sand\ssupplementary\sdata)', re.IGNORECASE)

            matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(text)])
            matches_array.columns = ['SearchTerm', 'Start']
            
            count = 0
            while count < (matches_array['SearchTerm'].count() - 1): # Can only iterate to the second last row
                matches_array.at[count,'Selection'] = (matches_array.iloc[count,0] + matches_array.iloc[count+1,0]).lower() # Convert to lower case
                count += 1
        
            
            matches_item7 = re.compile(r'(item\s7\.discussion\s[a-z]*)')
            matches_item8 = re.compile(r'(item\s8\.(consolidated\sfinancial|financial)\s[a-z]*)')
                
            Start = []
            End = []
                
            count = 0 
            while count < (matches_array['SearchTerm'].count() - 1):
                if re.match(matches_item7, matches_array.at[count,'Selection']):
                    Start.append(matches_array.iloc[count,1])

                if re.match(matches_item8, matches_array.at[count,'Selection']):
                    End.append(matches_array.iloc[count,1])
                count += 1

            return text[Start[1]:End[1]]

def main():
    dic_path = os.path.join("dictionaries", "LoughranMcDonald_MasterDictionary_2018.xlsx")
    master_dictionary = pd.read_excel(dic_path, index_col="Word", usecols=["Word", "Negative", "Positive"], engine="openpyxl")
    stop_words = os.path.join(dic_path, "StopWords_Generic.txt")
    for index in df.index:
        url = index
        response = requests.get(url)
        if response.status_code == 400 or response.status_code == 403:
            print("Server Error: Status Code ", response.status_code)
            print('skipping', df.at[index, "Company"], url)
            continue
        mda_text = parse(response.content)
        mda_analysis = Section(mda_text, master_dictionary, stop_words)
        for key in mda_analysis.variables:
            df.at[index, key] = mda_analysis.variables[key]
    df.to_csv("sec_edgar_completed_analysis.csv")

if __name__ == "__main__":
	main()