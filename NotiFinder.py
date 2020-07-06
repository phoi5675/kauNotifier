# -*- coding:utf-8 -*-
import requests
import const
from ExtractedNoti import *
from bs4 import BeautifulSoup
from datetime import date


class NotiFinder:
    def __init__(self, notiListWrapperClassKeyword, notiLineWrapperElementKeyword,
                 titleClassKeyword, dateClassKeyword, hrefElementKeyword, attributeKeyword):
        self.notiListWrapperClassKeyword = notiListWrapperClassKeyword
        self.notiLineWrapperElementKeyword = notiLineWrapperElementKeyword
        self.titleClassKeyword = titleClassKeyword
        self.dateClassKeyword = dateClassKeyword
        self.hrefElementKeyword = hrefElementKeyword
        self.attributeKeyword = attributeKeyword

    def findAllWrappedNotiLine(self, scrapedHtml):
        return scrapedHtml.find(class_=self.notiListWrapperClassKeyword).find_all(self.notiLineWrapperElementKeyword)

    def findTitleInString(self, wrappedNotiLine):
        try:
            foundTitleTag = wrappedNotiLine.find(attrs={self.attributeKeyword: self.titleClassKeyword})

            resultTitle = foundTitleTag.get_text()
            return resultTitle
        except AttributeError:
            return ''

    def findDateInString(self, wrappedNotiLine):
        try:
            foundDateTag = wrappedNotiLine.find(attrs={self.attributeKeyword: self.dateClassKeyword})
            if foundDateTag.span:
                foundDateTag.span.clear()

            resultDate = foundDateTag.get_text()
            return resultDate
        except AttributeError:
            return ''

    def findHrefInString(self, wrappedNotiLine):
        try:
            return wrappedNotiLine.a.get(self.hrefElementKeyword)
        except AttributeError:
            return ''

    @staticmethod
    def isToday(scrapDate):
        today = date.today().isoformat()
        if scrapDate == today:
            return True
        else:
            return False

    @staticmethod
    def webToLxmlClass(webPage):
        def removeBlank(html):
            html = html.replace("\t", "")
            html = html.replace("\n", "")
            html = html.replace("\r", "")

            return html

        requestedHtml = requests.get(webPage)
        textHtml = requestedHtml.text

        textHtml = removeBlank(textHtml)

        return BeautifulSoup(textHtml, 'lxml')


def webScrap(notiFinder, notiListAll, webPageList):
    for notiList, webPage in zip(notiListAll, webPageList):
        scrapedHtml = NotiFinder.webToLxmlClass(webPage)
        notiLines = notiFinder.findAllWrappedNotiLine(scrapedHtml)

        # 학교 홈페이지 공지와 학과 공지 배열이 다르므로 try except 문으로 해결
        try:
            notiList.category = const.GENWEBDICT[webPage]
        except KeyError:
            notiList.category = const.DEPWEBDICT[webPage]

        for notiLine in notiLines:
            date = notiFinder.findDateInString(notiLine)

            if NotiFinder.isToday(date):  # 오늘 날짜와 일치하는 공지만 추가
                title = notiFinder.findTitleInString(notiLine)
                # href 에는 게시물 id 만 포함
                href = notiFinder.findHrefInString(notiLine)

                notiList.extractedNotiList.append(ExtractedNoti(title, date, href))
                notiList.numOfNoti = notiList.numOfNoti + 1
            else:
                continue

