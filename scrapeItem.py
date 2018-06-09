# -*- coding: utf-8 -*-

from Class import entities
from Class import bean
from Class import scrapeYakkun
from Class import util
from Class import dao

def main():
    
    # URL取得
    itemURL = entities.WebPage.TETTEIKOURYAKU_ITEM
    soup = util.SoupUtil.getSoupFromURL(itemURL)
    itemURLZcrystal = scrapeYakkun.ScrapeItems.getURL(itemURL, soup, "Zクリスタル")
    itemURLMegastone = scrapeYakkun.ScrapeItems.getURL(itemURL, soup, "メガストーン")
    itemURLBerry = scrapeYakkun.ScrapeItems.getURL(itemURL, soup, "きのみ")
    
    # mysqlへの接続を指定
    with dao.Connector(entities.Dao.ACCOUNT) as connect:
        # 通常の道具、Zクリスタル、メガストーン、きのみ、それぞれでscrape
        for itemURLcategory in [itemURL, itemURLZcrystal, itemURLMegastone, itemURLBerry]:
            soupCategory = util.SoupUtil.getSoupFromURL(itemURLcategory)
            itemList = scrapeYakkun.ScrapeItems.getItemInfo(soupCategory)
            print("[ scrapeItem.py ] : ----------start scraping next item category----------")
            for itemInfo in itemList:
                dao.ItemDao.insertItemData(itemInfo, connect)
                print("[ scrapeItem.py ] : scraping: " + itemInfo[0])
        

if __name__ == '__main__':
    
    main()


