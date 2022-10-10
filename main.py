import os
import sys
import search
import string
import argparse
import requests
import xlsxwriter

import pandas as pd
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='변환하고자 하는 엑셀 파일의 폴더 위치')
    
output_folder = 'output'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}
url = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord="

def remove_space(title):
    return title.replace(" ", "")

def search_book_from_key(title, company):
    output = []
    _title = remove_space(title)    
    res = requests.get(url + title)
    
    if res.status_code == 200:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        
        search_result = soup.find("div", attrs={"id":"Search3_Result"})
        if search_result is None:
            return output
        books = search_result.find_all("div", attrs={"class":"ss_book_box"})
        if books is None:
            return output
        is_find = False     
        for book in books:
            if is_find == True:     
                break
            b_status = book.find("div", attrs={"class" : "book_Rfloat_02"}).find("div").get_text()
            b_list = book.find("div", attrs={"class" : "ss_book_list"}).find_all("li")
            
            b_price = ""
            b_title = ""
            b_company = ""
            b_authors = []
           
            for idx in range(len(b_list)):
                sale_price = b_list[idx].find("span", attrs={"class" : "ss_p2"}) # 할인가
                if sale_price != None:
                    price = b_list[idx].find("span") # 정가
                    b_price = price.get_text()
                                
                info = b_list[idx].find("a", attrs={"class" : "bo3"})
                if info != None:
                    b_title = info.get_text()
                    
                    detail = b_list[idx + 1].find_all("a")
                    b_authors = [author.get_text() for author in detail[:-1]]
                    b_company = detail[-1].get_text()

            _b_title = remove_space(b_title)
            if _b_title == _title and b_company == company:
                print("검색 결과 : "+_b_title, b_authors, b_company, b_price, b_status)
                output.append([_b_title, b_authors, b_company, b_price, b_status])
                is_find = True        
    return output

def highlight_rows(row):
    value = row.loc['상태']
    if value != '':
        color = 'background-color: yellow'
    else:
        color = ''
    return [color for r in row]

def remove_purchase_campany_info(df): # 견적서 정보 제거
    df = df[12:-1].reset_index(drop=True)
    df.columns = df.loc[0]
    df = df[1:]
    df['상태'] = ''
    return df

def open_excel_file(f_path):
    df = pd.read_excel(f_path, header=None, sheet_name=0)
    df = remove_purchase_campany_info(df)
    # test
    for i in range(1, 2):
        data = df.loc[i]
        title = data['도서명']
        comp = data['출판사']
        # try:
        bs = search.Booksearch(title, comp)
        bs.search_url(url)
        # except:
        #     print('exception error')    

def main(f_dir):
    if not os.path.exists(f_dir): 
        return print('Input directory is not exist. Please check input')
    
    f_list = os.listdir(f_dir)
    if len(f_list) == 0:
        return print('Empty directory')
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        
    # load excel 
    for f in f_list:
        f_path = os.path.join(f_dir,f)
        open_excel_file(f_path)
        
        
if __name__ == "__main__":
    args = parser.parse_args()
    main(args.input)