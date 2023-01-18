from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm
# Not required but nice to have
import re


def excel_prep(input_file):
    input_excel_df = pd.DataFrame(pd.read_excel(input_file))
    input_excel_df['URL'] = ''
    # Intakes xlsx file and adds a blank "URL" column
    for index, row in tqdm(input_excel_df.iterrows(), total=len(input_excel_df)):
        # Creates a url based on the "OPPORTUNITY NUMBER" column then checks if it is valid (status code 200). Finally,
        # it updates the dataframe and exports as an xlsx called output.xlsx
        value = row['OPPORTUNITY NUMBER']
        if value.startswith('RFA'):
            url = 'https://grants.nih.gov/grants/guide/rfa-files/' + value + '.html'
            url_test = requests.get(url)
            if url_test.status_code == 200:
                input_excel_df.at[index, 'URL'] = url
            else:
                input_excel_df.at[index, 'URL'] = 'No available file'
        elif value.startswith('PA'):
            url = 'https://grants.nih.gov/grants/guide/pa-files/' + value + '.html'
            url_test = requests.get(url)
            if url_test.status_code == 200:
                input_excel_df.at[index, 'URL'] = url
            else:
                input_excel_df.at[index, 'URL'] = 'No available file'
        elif value.startswith('RFI'):
            url = 'https://grants.nih.gov/grants/guide/notice-files/' + value + '.html'
            url_test = requests.get(url)
            if url_test.status_code == 200:
                input_excel_df.at[index, 'URL'] = url
            else:
                input_excel_df.at[index, 'URL'] = 'No available file'
        elif value.startswith('FOR'):
            url = 'No available file'
            input_excel_df.at[index, 'URL'] = url
        else:
            print(f'There was an error at{index}')
    input_excel_df.to_excel(r'./excel_files/output.xlsx', index=False)


def parse_data():
    input_excel_df = pd.DataFrame(pd.read_excel('./excel_files/output.xlsx'))
    input_excel_df['purpose'] = ''
    input_excel_df['text'] = ''
    # Intakes the xlsx file created in excel_prep and creates two blank columns
    for index, row in tqdm(input_excel_df.iterrows(), total=len(input_excel_df)):
        url = row['URL']
        try:
            if url == 'No available file':
                pass
            else:
                entry_html = requests.get(url).text
                soup = BeautifulSoup(entry_html, 'html.parser')
                checker1 = soup.find_all('div', class_='Section1')
                checker2 = soup.find_all('div', class_='container')
                checker3 = soup.find_all('div', class_='WordSection1')
                # checker1, 2, and 3 are hacky ways to identify which format the HTML files are in. The structure
                # examples are found in the readme file. I cannot figure out any possible explanation for why the format
                # changes
                if checker1:
                    try:
                        entry_html = requests.get(url).text
                        soup = BeautifulSoup(entry_html, 'html.parser')
                        heading = soup.find(class_='regulartextChar1', text='Purpose')
                        for element in heading.next_siblings:
                            # This avoids some html weirdness
                            purpose = ''
                            if str(element) == '<b><span>.</span></b>':
                                pass
                            elif str(element) == '<span class="regulartext"><b><span></span></b></span>':
                                pass
                            else:
                                purpose = str(element)
                            input_excel_df.at[index, 'purpose'] = purpose.text
                    except AttributeError as e:
                        print(e)
                        print('type1')
                        # Aids in troubleshooting
                        print(f'attribute error at {url}')
                elif checker2:
                    try:
                        entry_html = requests.get(url).text
                        soup = BeautifulSoup(entry_html, 'html.parser')
                        funding_op_purpose = soup.find('div', text=re.compile('Funding Opportunity Purpose'))
                        purpose = funding_op_purpose.find_next_sibling()
                        text_element = soup.find_all('div')
                        # If there is a warning here it's because I couldn't find a more elegant way to write this
                        # without duplicating lines

                        def parsley():
                            for text_scraped in text_element:
                                text_clean = text_scraped.get_text()
                                return text_clean
                        text = parsley()
                        index_1 = text.find('Full Text of Announcement')
                        text = text[index_1:]
                        index_2 = text.find('Section II')
                        text = text[:index_2]
                        input_excel_df.at[index, 'purpose'] = purpose.text
                        input_excel_df.at[index, 'text'] = text
                    except AttributeError as e:
                        print(e)
                        print('type2')
                        # Aids in troubleshooting
                        print(f'attribute error at {url}')
                elif checker3:
                    try:
                        entry_html = requests.get(url).text
                        soup = BeautifulSoup(entry_html, 'html.parser')
                        funding_op_purpose = soup.find('div', text='Funding Opportunity Purpose')
                        purpose = funding_op_purpose.find_next(class_='regulartext')
                        text_element = soup.find_all('div')
                        # If there is a warning here it's because I couldn't find a more elegant way to write this
                        # without duplicating lines

                        def parsley():
                            for text_scraped in text_element:
                                text_clean = text_scraped.get_text()
                                return text_clean
                        text = parsley()
                        index_1 = text.find('Full Text of Announcement')
                        text = text[index_1:]
                        index_2 = text.find('Section II')
                        text = text[:index_2]
                        input_excel_df.at[index, 'purpose'] = purpose.text
                        input_excel_df.at[index, 'text'] = text
                    except AttributeError as e:
                        print(e)
                        print('type3')
                        # Aids in troubleshooting
                        print(f'attribute error at {url}')
                else:
                    print(f'Could not detect site type for entry {index}')
        finally:
            pass
        input_excel_df.to_excel(r'./excel_files/output_final.xlsx', index=False)


if __name__ == '__main__':
    # excel_prep("./excel_files/input.xlsx")
    parse_data()
