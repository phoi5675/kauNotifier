BOARDID = "?search_boardId="
# 일반, 학사공지
GENERAL = "http://kau.ac.kr/page/kauspace/general_list.jsp" + "?search_boardId="  # 일반
ACADEMIC = "http://kau.ac.kr/page/kauspace/academicinfo_list.jsp" + "?search_boardId="  # 학사
SCHOLAR = "http://www.kau.ac.kr/page/kauspace/scholarship_list.jsp" + "?search_boardId="  # 장학 / 대출
RESEARCH = "http://www.kau.ac.kr/page/kauspace/research_list.jsp" + "?search_boardId="  # 산학 / 연구
EVENT = "http://www.kau.ac.kr/page/kauspace/event_list.jsp" + "?search_boardId="  # 행사
EMPLOY = "http://www.kau.ac.kr/page/kauspace/employment_list.jsp" + "?search_boardId="  # 모집 / 채용
CAREER = ["http://career.kau.ac.kr/ko/community"]  # 취업 -> 양식이 다르므로 따로 추가
CAREERAPPEND = ["http://career.kau.ac.kr"]  # 취업 -> 링크 붙이기 용도

# 학과공지
MACH = "http://www.kau.ac.kr/page/web/am_engineer/notice/dept_li.jsp" + "?search_boardId="  # 항우기
ELEC = "http://www.kau.ac.kr/page/dept/eie/board/undergraduate_notice.jsp" + "?search_boardId="  # 항전정
SOFT = "http://sw.kau.ac.kr/page_id=739"  # 소프트
STUF = "http://www.kau.ac.kr/page/web/aviation_stuff/notice/dept_li.jsp" + "?search_boardId="  # 재료
LAWS = "http://www.kau.ac.kr/page/web/universe_law/life/notice_li.jsp" + "?search_boardId="  # 교물
AVIA = "http://www.kau.ac.kr/page/web/aviation_service/information/no_dept_li.jsp" + "?search_boardId="  # 운항
BUSI = "http://www.kau.ac.kr/page/web/business/community/news_li.jsp" + "?search_boardId="  # 경영
FREE = "http://www.kau.ac.kr/page/school/free/notice/notice_li.jsp" + "?search_boardId="  # 자유

# 학교 전체 공지 링크 리스트
GENWEB = [GENERAL, ACADEMIC, SCHOLAR, RESEARCH, EVENT, EMPLOY]

# 학과 공지 배열 / 소프트 추가 X
DEPWEB = [MACH, ELEC, STUF, LAWS, AVIA, BUSI, FREE]

# 학교 전체 공지 배열 크기
GENINT = len(GENWEB)

# 학과 공지 배열 크기
DEPINT = len(DEPWEB)

# 파일 저장용 배열
DEPFIARY = ["mach", "elec", "stuf", "laws", "avia", "busi", "free"]

# 구글 스프레드시트 -> 파일 읽기
DEPDICT = {"항우기": "mach", "항전정": "elec", "재료": "stuf",
           "교물": "laws", "운항": "avia", "경영": "busi", "자유": "free"}

# -------------------- html -------------------- #
# 학교 전체 공지 딕셔너리
GENWEBDICT = {GENERAL: "일반", ACADEMIC: "학사", SCHOLAR: "장학 / 대출",
              RESEARCH: "산학 / 연구", EVENT: "행사", EMPLOY: "모집 / 채용", CAREER[0]: "취업"
}
# 학과 공지 딕셔너리
DEPWEBDICT = {MACH: "항공우주기계공학부", ELEC: "항공전자정보공학부", STUF: "재료공학부",
              LAWS: "항공교통물류학부", AVIA: "항공운항학과", BUSI: "경영학부", FREE: "자유전공학부"
}

# HTML 파일 베이스
HTMLBASE = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset=\"utf-8\">
    </head>
    <body>
    </body>
</html>
'''

# HTML 아래에 구독 신청 / 취소 등 정보를 위한 p 태그 및 신청 / 취소 링크
SUBSCRIBELINK = "https://forms.gle/WwL3GB57zbRq5PWG6"
UNSUBSCRIBELINK = "https://forms.gle/eHxyqZTD1HNA3u9SA"
MEMOSTRING = "공지알리미 버그 수정 및 코드 최적화 중입니다. 양식 변경 및 내용 표시에 오류가 발생 할 수 있으니 참고 바랍니다"
MAILLINK = "phoinotifier@gmail.com"
INFOTAG = '''
<p>
다른 학우분들도 메일을 받아 볼 수 있게 해주세요! 신청은 <a href=''' + SUBSCRIBELINK + '''>여기</a> 에서 할 수 있습니다<br>
구독을 중단하고 싶은 경우 <a href=''' + UNSUBSCRIBELINK + '''>여기</a>에 메일을 적어주세요<br>
기타 문의사항은 <a href=''' + MAILLINK + '''>''' + MAILLINK + '''</a>으로 문의 바랍니다<br>
''' + MEMOSTRING + '''
</p>
'''

# -------------------- 파일 -------------------- #
# 파일 경로 / 루트 폴더까지만 지정
# FILEPATH = "/home/phoi/Documents/web_scrap/"
FILEPATH = "./"

# -------------------- email 발송 -------------------- #
# json 파일 이름
JSON = '.json'

# 이메일 ID / PW
SENDERID = "@gmail.com"
SENDERPWD = "pwd"

# 스프레드시트 링크
SPREADSHEETLINK = "https://https://docs.google.com/spreadsheets/"

# 시트 이름
SHEETNAME = "설문지 응답 시트1"

# email 제목
EMAILTITLE = "항공대학교 공지사항"

# -------------------- deprecated values -------------------- #
GENFIARY = ["gen", "aca", "sch", "res", "eve", "emp", "car"]
