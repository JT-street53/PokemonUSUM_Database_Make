# -*- coding: utf-8 -*-

from Class import entities
from Class import bean
from Class import scrapeYakkun
from Class import util
from Class import dao

def main():
    
    # URL取得
    moveURL = entities.WebPage.TETTEIKOURYAKU_WAZA
    soup = util.SoupUtil.getSoupFromURL(moveURL)
    moveURLStatus = scrapeYakkun.ScrapeMoves.getURL(moveURL, soup, "変化")
    moveURLPhysical = scrapeYakkun.ScrapeMoves.getURL(moveURL, soup, "物理")
    moveURLSpecial = scrapeYakkun.ScrapeMoves.getURL(moveURL, soup, "特殊")
    
    # mysqlへの接続を指定
    with dao.Connector(entities.Dao.ACCOUNT) as connect:
        # 変化技、物理技、特殊技それぞれでscrape
        for moveURLCategory in [moveURLStatus, moveURLPhysical, moveURLSpecial]:
            soupCategory = util.SoupUtil.getSoupFromURL(moveURLCategory)
            trListCategory = scrapeYakkun.ScrapeMoves.getTrList(soupCategory)
            print("[ scrapeMoves.py ] : ----------start scraping next move category----------")
            for tr in trListCategory:
                moveBean = bean.MoveBean()
                moveBean = scrapeYakkun.ScrapeMoves.getMoveData(tr, moveBean)

                dao.MoveDao.insertMoveData(moveBean, connect)
                
                print("[ scrapeMoves.py ] : scraping: " + moveBean.name)
        

if __name__ == '__main__':
    
    main()


