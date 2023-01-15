from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm


def excel_prep(input_file):
    input_excel_df = pd.DataFrame(pd.read_excel(input_file))
    input_excel_df['URL'] = ''
    for index, row in tqdm(input_excel_df.iterrows(), total=len(input_excel_df)):
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
    input_excel_df.to_excel(r'./output.xlsx', index=False)


def parse_data():
    input_excel_df = pd.DataFrame(pd.read_excel('output.xlsx'))
    input_excel_df['purpose'] = ''
    input_excel_df['text'] = ''
    for index, row in tqdm(input_excel_df.iterrows(), total=len(input_excel_df)):
        url = row['URL']
        try:
            if url == 'No available file':
                pass
            else:
                entry_html = requests.get(url).text
                soup = BeautifulSoup(entry_html, 'html.parser')
                checker1 = soup.find('div', class_='Section1')
                checker2 = soup.find('div', class_='container')
                checker3 = soup.find('div', class_='WordSection1')
                if checker1:
                    try:
                        entry_html = requests.get(url).text
                        soup = BeautifulSoup(entry_html, 'html.parser')
                        heading = soup.find(class_='regulartextChar1', text='Purpose')
                        for element in heading.next_siblings:
                            purpose = ''
                            if str(element) == '<b><span>.</span></b>':
                                pass
                            elif str(element) == '<span class="regulartext"><b><span></span></b></span>':
                                pass
                            else:
                                purpose = str(element)
                            input_excel_df.at[index, 'purpose'] = purpose
                    except AttributeError:
                        print('type1')
                        print(f'attribute error at {url}')
                elif checker2:
                    # Type 2 files match the Type_2_format (found in readme)
                    try:
                        entry_html = requests.get(url).text
                        soup = BeautifulSoup(entry_html, 'html.parser')
                        funding_op_purpose = soup.find('div', text='Funding Opportunity Purpose')
                        purpose = funding_op_purpose.find_next_sibling()
                        text_element = soup.find_all('div')

                        def parsley():
                            for text_scraped in text_element:
                                text_clean = text_scraped.get_text()
                                return text_clean
                        text = parsley()
                        index_1 = text.find('Full Text of Announcement')
                        text = text[index_1:]
                        index_2 = text.find('Section II')
                        text = text[:index_2]
                        input_excel_df.at[index, 'purpose'] = purpose
                        input_excel_df.at[index, 'text'] = text
                    except AttributeError as e:
                        print(e)
                        print('type2')
                        print(f'attribute error at {url}')
                elif checker3:
                    # Type 3 files match the Type_3_format (found in readme)
                    try:
                        entry_html = requests.get(url).text
                        soup = BeautifulSoup(entry_html, 'html.parser')
                        funding_op_purpose = soup.find('div', text='Funding Opportunity Purpose')
                        purpose = funding_op_purpose.find_next(class_='regulartext')
                        text_element = soup.find_all('div')

                        def parsley():
                            for text_scraped in text_element:
                                text_clean = text_scraped.get_text()
                                return text_clean
                        text = parsley()
                        index_1 = text.find('Full Text of Announcement')
                        text = text[index_1:]
                        index_2 = text.find('Section II')
                        text = text[:index_2]
                        input_excel_df.at[index, 'purpose'] = purpose
                        input_excel_df.at[index, 'text'] = text
                    except AttributeError:
                        print('type3')
                        print(f'attribute error at {url}')
                    else:
                        print(f'Could not detect site type for entry {index}')
        finally:
            pass
        input_excel_df.to_excel(r'./output1.xlsx', index=False)

# def parse_type_1(url):
#     # Type 1 files match the Type_1_format (found in readme), there is no discernible reason for the formatting choices
#     try:
#         entry_html = requests.get(url).text
#         soup = BeautifulSoup(entry_html, 'html.parser')
#         heading = soup.find(class_='regulartextChar1', text='Purpose')
#         for element in heading.next_siblings:
#             purpose = ''
#             if str(element) == '<b><span>.</span></b>':
#                 pass
#             elif str(element) == '<span class="regulartext"><b><span></span></b></span>':
#                 pass
#             else:
#                 purpose = str(element)
#             return purpose
#     except AttributeError:
#         print('type1')
#         print(f'attribute error at {url}')


# def parse_type_2(url):
#     # Type 2 files match the Type_2_format (found in readme), there is no discernible reason for the formatting choices
#     try:
#         entry_html = requests.get(url).text
#         soup = BeautifulSoup(entry_html, 'html.parser')
#         funding_op_purpose = soup.find('div', text='Funding Opportunity Purpose')
#         purpose = funding_op_purpose.find_next_sibling()
#         text_element = soup.find_all('div')
#
#         def parsley():
#             for text_scraped in text_element:
#                 text_clean = text_scraped.get_text()
#                 return text_clean
#         text = parsley()
#         index_1 = text.find('Full Text of Announcement')
#         text = text[index_1:]
#         index_2 = text.find('Section II')
#         text = text[:index_2]
#         # print(purpose, text)
#     except AttributeError as e:
#         print(e)
#         print('type2')
#         print(f'attribute error at {url}')


# def parse_type_3(url):
#     # Type 3 files match the Type_3_format (found in readme), there is no discernible reason for the formatting choices
#     try:
#         entry_html = requests.get(url).text
#         soup = BeautifulSoup(entry_html, 'html.parser')
#         funding_op_purpose = soup.find('div', text='Funding Opportunity Purpose')
#         purpose = funding_op_purpose.find_next(class_='regulartext')
#         text_element = soup.find_all('div')
#
#         def parsley():
#             for text_scraped in text_element:
#                 text_clean = text_scraped.get_text()
#                 return text_clean
#         text = parsley()
#         index_1 = text.find('Full Text of Announcement')
#         text = text[index_1:]
#         index_2 = text.find('Section II')
#         text = text[:index_2]
#         # print(purpose, text)
#     except AttributeError:
#         print('type3')
#         print(f'attribute error at {url}')


if __name__ == '__main__':
    # excel_prep("input.xlsx")
    parse_data()
