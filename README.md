# Deprecated
통합 공지 프로그램 "univNotifier" 로 병합되었습니다.
https://github.com/phoi5675/univNotifier

# kauNotifier
kau.ac.kr 의 공지사항을 매일 오후 9시에 메일로 받아볼 수 있습니다

페이지 뷰 방식이 다른 과와 차이가 있는 소프트웨어 학부의 공지는 지원하지 않습니다. 추후 지원 예정
# Requirements
- python3 (2.7.x 에서는 unicode 오류 가능성 있음)
- requests
- datetime
- bs4 (Beautifulsoup)
- gspread
- oauth2client
- email
- smtplib
# Sources
- 웹 스크래핑
  - https://github.com/Space4all/kau-notify (kau.ac.kr 에서 board_id 를 이용하여 페이지 이동하는 부분)
  - https://www.crummy.com/software/BeautifulSoup/bs4/doc/ (beautifulsoup documentation)
- email 발송
  - http://hleecaster.com/python-email-automation/ (파이썬 이메일 자동화)
  - https://stackoverflow.com/questions/882712/sending-html-email-using-python (html 형식으로 메일 발송)
  - http://hleecaster.com/python-google-drive-spreadsheet-api/ (파이썬에서 구글 스프레드시트 이용)
# License
MIT License. For more information, see LICENSE.
