#-*- coding:utf-8 -*-
import requests
from datetime import date
from bs4 import BeautifulSoup
class board():
    def __init__(self, title, date, board_id, board_name):
        self.title = title
        self.date = date
        self.board_id = board_id
        self.board_name = board_name
def scrap(web_index, board_name, mlist):
    '''
    사이트에서 게시물 추출하는 부분
    '''
    # request web addr and prettify html
    r = requests.get(web_index)
    res = r.text
    res.lstrip()
    soup = BeautifulSoup(res, 'lxml')

    has_noti = 0 # 공지가 존재하는지 확인하는 변수

    '''
    게시물의 각 제목은 <tbody> 태그 내의 <tr> 태그로 감싸져 있으므로
    <tbody> 를 먼저 뽑아낸 후, 각각 게시물의 (타이틀 / id(링크) / 날짜)를 추출 후, 오늘 날짜와 일치하는지 확인
    오늘 날짜와 일치하는 경우만 리스트에 뽑음
    '''
    tbody = soup.find("tbody")
    tr_list = tbody.find_all('tr')
    for tr in tr_list:
        temp_title = tr.find(headers='board_title').get('title')  # 타이틀 추출
        temp_date = tr.find(headers='board_create').get_text()  # 게시물 날짜 추출
        # 게시물 id 추출
        temp_id = (str)(tr.a)
        temp_id = temp_id[(temp_id.find('(') + 1):temp_id.find(',')]
        temp_id_res = web_index + boardId + temp_id
        # 오늘 날짜와 일치하는 경우, 리스트에 추가
        if temp_date == today:
        #if temp_date == '2020-03-30': # 테스트용
            mlist.append(board(temp_title, temp_date, temp_id_res, board_name))
            has_noti += 1
    if has_noti > 0:
        return 1
    else:
        return 0

boardId = "?search_boardId="

# 일반, 학사공지
GENERAL = "http://kau.ac.kr/page/kauspace/general_list.jsp" # 일반
ACADEMIC = "http://kau.ac.kr/page/kauspace/academicinfo_list.jsp" # 학사
SCHOLAR = "http://www.kau.ac.kr/page/kauspace/scholarship_list.jsp" # 장학 / 대출
RESEARCH = "http://www.kau.ac.kr/page/kauspace/research_list.jsp" # 산학 / 연구
EVENT = "http://www.kau.ac.kr/page/kauspace/event_list.jsp" # 행사
EMPLOY = "http://www.kau.ac.kr/page/kauspace/employment_list.jsp" # 모집 / 채용

# 학과공지
MACH = "http://www.kau.ac.kr/page/web/am_engineer/notice/dept_li.jsp"  # 항우기
ELEC = "http://www.kau.ac.kr/page/dept/eie/board/undergraduate_notice.jsp"  # 항전정
SOFT = "http://sw.kau.ac.kr/page_id=739"  # 소프트
STUF = "http://www.kau.ac.kr/page/web/aviation_stuff/notice/dept_li.jsp"  # 재료
LAWS = "http://www.kau.ac.kr/page/web/universe_law/life/notice_li.jsp"  # 교물
AVIA = "http://www.kau.ac.kr/page/web/aviation_service/information/no_dept_li.jsp"  # 운항
BUSI = "http://www.kau.ac.kr/page/web/business/community/news_li.jsp"  # 경영
FREE = "http://www.kau.ac.kr/page/school/free/notice/notice_li.jsp"  # 자유

# 소프트는 게시판 방식이 다르므로 나중에 따로 추가
# 능력자분이 해주시겠지 뭐,,,
# 일반 공지
gen_noti = ["gen", "aca", "sch", "res", "eve", "emp"]
gen_web_arr = [GENERAL, ACADEMIC, SCHOLAR, RESEARCH, EVENT, EMPLOY]
gen_noti_count = 0 # 일반 공지 전체 카운트 변수
# 학부별 공지
dept_noti = ["mach", "elec", "stuf", "laws", "avia", "busi", "free"]
dept_web_arr = [MACH, ELEC, STUF, LAWS, AVIA, BUSI, FREE]
dept_noti_count = list(0 for i in range(len(dept_web_arr))) # 학부별 공지 카운트 변수

gen_list = list(list() for i in range(len(gen_web_arr)))
dept_list = list(list() for i in range(len(dept_web_arr)))


# 오늘 날짜 확인
today = date.today().isoformat()
file_out = []

# 일반공지
for gen_web_index, gen_index, gen_list_index in zip(gen_web_arr, gen_noti, gen_list):
    # 오늘의 학교 홈페이지 공지사항을 gen_list 에 저장
    if scrap(gen_web_index, gen_noti, gen_list_index):
        gen_noti_count += 1

# 각 학과별 학과공지
for dept_web_index, dept_noti_index, dept_index in zip(dept_web_arr, dept_noti, dept_list):
    # 오늘의 학과 공지사항을 dept_list 에 저장
    if scrap(dept_web_index, dept_noti_index, dept_index):
        dept_noti_count[dept_web_arr.index(dept_web_index)] += 1

# 파일로 내보내기
html_text = '''
<!DOCTYPE html>
<html>

<head>
    <meta charset=\"utf-8\">
    <title>Kau Notifier</title>
</head>

<body>
    <h1>항공대학교 공지사항</h1><br>
    <h2>일반공지<br></h2>
    <h3>학과공지<br></h3>
    <p>구독을 중단하고 싶은 경우<br>phoiNotifier@gmail.com<br>으로 메일을 보내주시기 바랍니다.</p>
</body>

</html>'''
for dept_index, dept_file, dept_noti_count_index in zip(dept_list, dept_noti, dept_noti_count):
    html_base = BeautifulSoup(html_text, 'lxml')
    br = html_base.new_tag("br")
    # 공지를 html 에 추가하는 부분을 함수로 만들면 훨씬 코드가 깔끔하겠지만 그냥 쓰자
    # 일반공지 먼저 추가
    for gen_index in gen_list:
        for i in range(0, len(gen_index)):
            h2 = html_base.h2

            # 타이틀과 링크를 추가
            new_tag = html_base.new_tag('a', href=gen_index[i].board_id)
            new_tag.string = gen_index[i].title
            new_tag.append(br)
            h2.insert_after(new_tag)

    # 학과공지 추가
    # 학과 공지 개수가 1개 이상일 수 있으므로 루프를 하나 더 생성해서, 학과 공지 "목록"을 html 에 추가
    if dept_noti_count_index != 0:
        for i in range(0, len(dept_index)):
            # 학과 공지글이 없는 경우, 과정 생략
            h3 = html_base.h3

            # 타이틀과 링크를 추가
            new_tag = html_base.new_tag('a', href=dept_index[i].board_id)
            new_tag.string = dept_index[i].title
            new_tag.append(br)
            h3.insert_after(new_tag)
    if (dept_noti_count_index != 0) or (gen_noti_count != 0):
        # 파일에 저장하기 / 왜 with open 은 오류가 나는건지?`
        # 학교 / 학부 공지 중 하나 이상이 존재하는 경우에만 파일 생성
        fi = open('./html/' + dept_file + '.html', 'w')  # 파일 오픈
        fi.write((str)(html_base))
        fi.close()
