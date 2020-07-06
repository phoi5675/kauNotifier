#-*- coding:utf-8 -*-
import requests
from datetime import date
from bs4 import BeautifulSoup
import const
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
    boardId = "?search_boardId="
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

# 취업공지 스크랩
def career_scrap(web_index, board_name, mlist):
    # request web addr and prettify html
    r = requests.get(web_index)
    res = r.text
    res.lstrip()
    soup = BeautifulSoup(res, 'lxml')

    has_noti = 0 # 공지가 존재하는지 확인하는 변수

    ul = soup.find("ul", class_="black")
    li_list = ul.find_all('li') # 공지 페이지에서 공지를 리스트로 추가

    for li in li_list:
        # 게시물 분류 부분에서 오류가 생기지만, 태그를 제거하는 것보다 이게 위험하지만 편하니까 try except 사용
        try:
            # 게시물 날짜 추출
            date_xml = li.find('time')
            temp_date = date_xml.get_text()
            # 게시물 링크 추출
            temp_id = "http://career.kau.ac.kr/" + li.a.get("href")
            # 게시물 제목 추출
            temp_title = li.a.get_text()

            # 오늘 날짜와 일치하는 경우, 리스트에 추가
            if temp_date == today:
            #if temp_date == '2020-03-16': # 테스트용
                mlist.append(board(temp_title, temp_date, temp_id, board_name))
                has_noti += 1
        except:
            pass

    if has_noti > 0:
        return 1
    else:
        return 0


def add_noti(html_base, cls, noti):
    div = html_base.find(class_=cls)

    # 타이틀과 링크를 추가
    new_tag = html_base.new_tag('a', href=noti.board_id)
    new_tag.string = noti.title
    new_tag.append(html_base.new_tag("br"))
    div.insert_after(new_tag)

# 메인함수 시작
if __name__ == '__main__':
    # 학부 / 학과별 공지를 저장할 배열
    gen_list = list(list() for i in range(len(const.KAUARY)))
    dept_list = list(list() for i in range(len(const.DEPARY)))

    gen_noti_count = 0  # 일반 공지 전체 카운트 변수
    dept_noti_count = list(0 for i in range(len(const.DEPARY)))  # 학부별 공지 카운트 변수

    # 오늘 날짜 확인
    today = date.today().isoformat()
    file_out = []

    # 일반공지
    for gen_web_index, gen_index, gen_list_index in zip(const.KAUARY, const.GENFIARY, gen_list):
        # 취업 공지의 경우, 페이지 뷰 방식이 다르므로 따로 제작
        if gen_index == "car":
            if career_scrap(gen_web_index, const.GENFIARY, gen_list_index):
                gen_noti_count += 1
        # 오늘의 학교 홈페이지 공지사항을 gen_list 에 저장
        elif scrap(gen_web_index, const.GENFIARY, gen_list_index):
            gen_noti_count += 1

    # 각 학과별 학과공지
    for dept_web_index, dept_noti_index, dept_index in zip(const.DEPARY, const.DEPFIARY, dept_list):
        # 오늘의 학과 공지사항을 dept_list 에 저장
        if scrap(dept_web_index, dept_noti_index, dept_index):
            dept_noti_count[const.DEPARY.index(dept_web_index)] += 1

    # 파일로 내보내기
    html_text = '''
    <!DOCTYPE html>
    <html>
    
    <head>
        <meta charset=\"utf-8\">
        <title>KAU Notifier</title>
    </head>
    
    <body>
        <h1>항공대학교 공지사항</h1><br>
        <h2>일반공지<br></h2>
            <div class="general"></div>
        <h2>학과공지<br></h2>
            <div class="dept"></div>
        <p>다른 학우분들도 메일을 받아 볼 수 있게 해주세요! 신청은 <a href="https://forms.gle/WwL3GB57zbRq5PWG6">여기</a> 에서 할 수 있습니다<br>
            <br>구독을 중단하고 싶은 경우 phoiNotifier@gmail.com 으로 메일을 보내주시기 바랍니다
            <br>구독을 중단하고 싶은 경우 <a href="https://forms.gle/eHxyqZTD1HNA3u9SA">여기</a>에 메일을 적어주시거나
            <br>phoiKAUNotifier@gmail.com 으로 메일을 보내주시기 바랍니다
        </p>

    </body>
    
    </html>'''

    # 아래는 나중에 추가 예정
    '''
    <p>구독을 중단하고 싶은 경우 <a href="https://forms.gle/eHxyqZTD1HNA3u9SA">여기</a>에 메일을 적어주시거나
            <br>phoiKAUNotifier@gmail.com 으로 메일을 보내주시기 바랍니다
        </p>
    '''
    for dept_index, dept_file, dept_noti_count_index in zip(dept_list, const.DEPFIARY, dept_noti_count):
        html_base = BeautifulSoup(html_text, 'lxml')
        # 일반공지 먼저 추가
        for gen_index in gen_list:
            for i in range(0, len(gen_index)):
                add_noti(html_base, "general", gen_index[i])

        # 학과공지 추가
        # 학과 공지 개수가 1개 이상일 수 있으므로 루프를 하나 더 생성해서, 학과 공지 "목록"을 html 에 추가
        if dept_noti_count_index != 0:
            for i in range(0, len(dept_index)):
                # 학과 공지글이 없는 경우, 과정 생략
                add_noti(html_base, "dept", dept_index[i])
        elif dept_noti_count_index == 0:
            # 학과 공지사항이 없는 경우, 없다는 문장 추가
            div = html_base.find(class_="dept")

            new_tag = html_base.new_tag('p')
            new_tag.string = "오늘은 학과 공지사항이 없습니다"
            new_tag.append(html_base.new_tag("br"))
            div.insert_after(new_tag)

        if (dept_noti_count_index != 0) or (gen_noti_count != 0):
            # 파일에 저장하기 / 왜 with open 은 오류가 나는건지?`
            # 학교 / 학부 공지 중 하나 이상이 존재하는 경우에만 파일 생성
            fi = open(const.FILEPATH + 'html/' + dept_file + '.html', 'w')  # 파일 오픈
            fi.write(str(html_base))
            fi.close()
