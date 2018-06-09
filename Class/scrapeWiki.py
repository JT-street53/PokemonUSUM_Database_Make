# -*- coding: utf-8 -*-

import time
import urllib
import re
from Class import entities
from Class import util
from Class import dao

# gif画像、ミニ画像を保存するクラス
class ScrapeWiki:

    # main
    def scrape(soup, englishName, connect):
        # 通常色
        ScrapeWiki.scrapeOrdinaryColorGif(soup, englishName, connect)
        # 色違い
        ScrapeWiki.scrapeShinyColorGif(soup, englishName, connect)
        
    # 通常フォルム
    def scrapeOrdinaryColorGif(soup, englishName, connect):
        if soup.find(id=re.compile("Sprites")) != None:
            table = soup.find(id=re.compile("Sprites")).next_element.next_element.next_element
        elif soup.find(id=re.compile("3D_Models")) != None:
            table = soup.find(id=re.compile("3D_Models")).next_element.next_element.next_element
        else:
            print("[ scrapeWiki.py ]: no table named Sprite or 3D Models")
            return
        
        imgs = table.find_all("img")
        for img in imgs:
            if img.get("alt") != None:
                if "XY" in img.get("alt") or "SM" in img.get("alt") or "USUM" in img.get("alt") or "Xy" in img.get("alt") or "Sm" in img.get("alt"):
                    try:
                        data = urllib.request.urlopen(img.get("data-src")).read()
                        time.sleep(1)
                        dexNum = dao.WikiDao.getDexNumberbyEnglishName(englishName, connect)
                        fname = '{0:04d}'.format(dexNum) + "00" + ".gif"
                        dst_path = entities.WebPage.WIKI_TOP_DIRECTORY + fname
                        with open(dst_path, mode="wb") as f:
                            f.write(data)
                        return
                    except urllib.error.URLError as e:
                        print(e)
                        return
                      
    # 色違い
    def scrapeShinyColorGif(soup, englishName, connect):
        imgs = soup.find_all("img")
        for img in imgs:
            if img.get("alt") != None:
                if "Shiny" in img.get("alt"):
                    if "XY" in img.get("alt") or "SM" in img.get("alt") or "USUM" in img.get("alt") or "Xy" in img.get("alt") or "Sm" in img.get("alt"):
                        try:
                            data = urllib.request.urlopen(img.get("data-src")).read()
                            time.sleep(1)
                            dexNum = dao.WikiDao.getDexNumberbyEnglishName(englishName, connect)
                            fname = '{0:04d}'.format(dexNum) + "00s" + ".gif"
                            dst_path = entities.WebPage.WIKI_TOP_DIRECTORY + fname
                            with open(dst_path, mode="wb") as f:
                                f.write(data)
                            return
                        except urllib.error.URLError as e:
                            print(e)
                            return