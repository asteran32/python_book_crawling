import os
import sys
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

def remove_space(title): # 제목에서 공백제거
    _title = ''
    for t in list(title):  
        if t.isalpha(): # 영문자 소문자 변환
            t = t.lower()
        if t == ' ':
            continue
        _title += t
    return _title

def search_keyword(title, company):
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

if __name__ == "__main__":
    args = parser.parse_args()
    
    file_path = args.input
    if not os.path.exists(file_path):
        print('해당 폴더가 없습니다')
        sys.exit()

    files = os.listdir(file_path)
    if len(files) == 0:
        print('폴더 내부에 파일이 존재하지 않습니다 ..')
        sys.exit()
    
    if not os.path.exists(output_folder):
        print('새폴더를 생성합니다 ..')
        os.mkdir(output_folder)
    
    print('알라딘 접속 시도 ..')
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print('해당 URL에 접속할 수 없습니다 .. Error code:' + str(res.status_code))
        sys.exit()

    for f in files:
        input_file_path = os.path.join(file_path, f)
        
        print('{} 검색을 시작합니다 ...'.format(input_file_path))

        dataframe = pd.read_excel(input_file_path, header=None, sheet_name=0)
        if len(dataframe) == 0:
            print('빈 파일입니다')
            continue

        # 상단 견적서, 하단 합계 제거, 셀 추가
        df = dataframe[12:-1]
        df = df.reset_index(drop=True)
        df.columns = df.loc[0]
        df = df[1:]
        df['상태'] = ''

        dt = df.copy()
        dt_length = len(dt)

        for idx in range(1, dt_length + 1):
            
            data = dt.loc[idx]
            print('검색 도서명: {} 출판사: {}'.format(data['도서명'], data['출판사']))
            try:
                output = search_keyword(data['도서명'], data['출판사'])   
                if len(output) == 0:
                    dt.loc[idx, '상태'] = "검색불가"
                    continue        
                if len(output) == 1:
                    output = output[0]
                if len(output) > 1:
                    for result in output:
                        if result[0] == data['도서명'] and result[2] == data['출판사']:
                            output = result
                
                b_title = output[0]
                b_company = output[2]
                b_status = output[4]
                b_price = ''    
                for p in output[3].split(','): # 금액에 쉼표 제거
                    b_price += p
                
                if b_price != str(data['정가']):
                    dt.loc[idx, '상태'] = '가격 불일치: ' + b_price
                if b_status != '장바구니':
                    dt.loc[idx, '상태'] = b_status
                
            except:
                print('검색 실패 ...')
                dt.loc[idx, '상태'] = '검색 실패'
             
        # 검색 결과 하이라이팅, 저장
        print('{} 파일 검색 결과를 저장합니다 ..'.format(f))      
        output_path = os.path.join(output_folder, f) + "x"; # for xlsx
        dt.style.apply(highlight_rows, axis=1).to_excel(output_path, engine='xlsxwriter' ,index=False)
        print('파일을 성공적으로 저장했습니다 : {}'.format(output_path))

