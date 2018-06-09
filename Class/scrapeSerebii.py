# -*- coding: utf-8 -*-
# 2018/4/28 decided not to use serebii.net!!!
from . import entities
from . import util

# Serebii.netのページに対してスクレイピングかける際のメソッドを集めたクラス
class ScrapeSerebii:
    
    # main, 引き数（）戻り値（タイプ、種族値、通常フォルム(boolean)）
    def scrape(url, connect):
        typeList = None
        baseStatsList = None
        normalFormList = None
        
        formNum = 333333333333333333
        
        soup = util.SoupUtil.getSoupFromURL(url)
        
        typeList = ScrapeSerebii.scrapeType(soup, connect)
        
        return typeList, baseStatsList, normalFormList
    
    # タイプ
    def scrapeType(soup, connect):
        answer = []
        div = soup.find("td", {"class" : "cen"})
        # フォルムが複数ある場合
        if div.find("table") != None:
            part = div.find("table")
            tdList = part.find_all("td")
            for td in tdList:
                imgs = td.find_all("img")
                if len(imgs) == 0:
                    continue
                typeList = []
                for img in imgs:
                    typeName = img.get("src").split("/")[-1].replace(".gif", "")
                    typeNameJ = entities.Convert.TYPE_DICTIONARY_J[typeName.upper()]
                    typeId = util.DaoUtil.insertDataAndGetID(typeNameJ)
                    typeList.append(typeId)
                answer.append(typeList)
        return answer
    
    # 種族値
    def scrapeBaseStats():
        
        return
    
    # 図鑑番号取得
    def scrapeDexNumber(soup):
        for tr in soup.find_all("tr"):
            if tr.get_text().find("National") > -1:
                dexNum = tr.find_all("td")[-1].get_text().replace("#","")
        return int(dexNum)
    
    # フォルムがいくつあるか探索
    def checkDatabase(soup, connect):
        
        return
    