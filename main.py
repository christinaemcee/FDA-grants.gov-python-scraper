import re
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests

pd.set_option('display.max_colwidth', None)

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




def parse_overview(par):
    input_excel = pd.DataFrame(pd.read_excel("input.xlsx"))
    if 'RFA' in input_excel['OPPORTUNITY NUMBER']:
        url = 'https://grants.nih.gov/grants/guide/rfa-files/' + input_excel['OPPORTUNITY NUMBER'] + '.html'
    elif 'RFA' in input_excel['OPPORTUNITY NUMBER']:
        url = 'https://grants.nih.gov/grants/guide/pa-files/' + input_excel['OPPORTUNITY NUMBER'] + '.html'

    elif 'FOR' in input_excel['OPPORTUNITY NUMBER']:
        input_excel['url'] = url
        print(input_excel)
    # for i in input_excel['url']:
    #     html_doc = requests.get(i).text
    #     soup = BeautifulSoup(html_doc, 'html.parser')
    #     # print(soup.find_all(class_='datacolumn'))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_overview('PAR-23-072')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
