# -*- coding: utf-8 -*-

from Class import entities
from Class import dao
from Class import util
from Class import scrapeWiki

def scrape(url, englishName, connect):
    # get soup
    soup = util.SoupUtil.getSoupFromURL(url)
    # scrape ordinary gif
    scrapeWiki.ScrapeWiki.scrape(soup, englishName, connect)
    print("[ scrapeImages.py ] : scraping&downloading ★★★ " + englishName + " ★★★")

def main():
    # mysqlへの接続を指定
    with dao.Connector(entities.Dao.ACCOUNT) as connect:
        # 英語名のリストを取得
        englishNameList = dao.WikiDao.getEnglishNameList(connect)
        for engName in englishNameList:
            url = entities.WebPage.POKEMON_WIKI + engName[0]
            scrape(url, engName[0], connect)
    print("[ scrapeImages.py ] : ************finished scraping&installing.************")

if __name__ == '__main__':

    main()

