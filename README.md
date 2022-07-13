# python book crawling

알라딘(www.aladin.co.kr)에서 도서를 검색해 견적서 엑셀에 기재된 정보와 일치하는지 확인하는 스크립트

1-12행까지 거래처 상세정보가 존재하며 13행에는 컬럼명이 존재

순서는 동일하지 않아도 되나 ‘도서명’, ‘출판사’, ‘저자’, ‘정가’ 가 존재해야 함

스크립트는 아래 명령어를 명령 프롬프트에서 치면 됨

```bash
cd '~/main.py folder path'
main.py --input 'xlsx file folder path'
```

견적서의 ‘도서명’ 을 검색하고 검색결과의 정가 가격과 견적서의 ‘정가’가 동일한지 확인

- 일치 → I열에 아무것도 기재 안함
- 불일치 → I열에 ‘가격불일치 : 검색된 가격표기’

견적서의 ‘도서명’을 검색하고 검색 결과를 찾지 못했을 때

- I열에 ‘검색불가’ 표기