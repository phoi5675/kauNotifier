# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import const
import copy
from ExtractedNoti import *
from NotiFinder import *
from NotiMaker import *

if __name__ == '__main__':
    genNotiListAll = list(ExtractedNotiList() for i in range(const.GENINT))
    deptNotiListAll = list(ExtractedNotiList() for i in range(const.DEPINT))

    notiFinder = NotiFinder('board_list', 'tr', 'board_title', 'board_create', 'href', 'headers')

    # 취업공지는 따로 생성 / 호환성을 위해 리스트로 생성
    careerNotiListAll = list(ExtractedNotiList() for i in range(len(const.CAREER)))
    notiFinderCareer = NotiFinder('black', 'li', 'title', 'reg_date', 'href', 'class')

    # 일반 공지 스크랩
    webScrap(notiFinder, genNotiListAll, const.GENWEB)

    # 취업 공지 스크랩
    webScrap(notiFinderCareer, careerNotiListAll, const.CAREER)

    # 학과 공지 스크랩
    webScrap(notiFinder, deptNotiListAll, const.DEPWEB)

    # href 수정
    # 취업 공지를 제외한 나머지 학교 / 학과 공지는 BoardId 값 따로 추출 필요
    addWebPageLinkToHrefList(genNotiListAll, const.GENWEB, True)
    addWebPageLinkToHrefList(deptNotiListAll, const.DEPWEB, True)
    # 취업 공지는 BoardId 값 추출 필요 없음
    addWebPageLinkToHrefList(careerNotiListAll, const.CAREERAPPEND, False)

    # 취업 공지를 일반 공지로 넘기기
    genNotiListAll.append(careerNotiListAll[0])

    # 받은 공지를 html 로 넘기기
    htmlBaseInString = const.HTMLBASE
    htmlBase = BeautifulSoup(htmlBaseInString, 'lxml')

    # 학교 일반 공지 전체 추가
    for singleCategoryNotiList in genNotiListAll:
        addCategoryNotiToHtml(singleCategoryNotiList, htmlBase)

    # 학과 공지
    for singleCategoryNotiList, filename in zip(deptNotiListAll, const.DEPFIARY):
        # 0. 공지가 없는 경우 루프 패스 / 이건 왜 안 넣었지
        if not isBodyTagContainsElements(htmlBase) and singleCategoryNotiList.numOfNoti == 0:
            continue
        # 1. copy 를 이용하여 일반 공지를 담은 htmlBase 를 유지한 채 htmlToSaveDeptNoti 에 htmlBase 내용 복사
        #    n 번째 루프에서는 덮어쓰기
        htmlToSaveDeptNoti = copy.copy(htmlBase)

        # 2. 한 학과의 공지를 htmlToSaveDeptNoti 에 저장
        addCategoryNotiToHtml(singleCategoryNotiList, htmlToSaveDeptNoti)

        # 3. INFOTAG 추가
        addInfoTag(htmlToSaveDeptNoti)

        # 4. htmlBase 를 학과 파일로 저장
        htmlToFile(htmlToSaveDeptNoti, filename)
