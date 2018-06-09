# -*- coding: utf-8 -*-

from . import entities
from . import bean
from . import util
from . import dao
import re
import requests
import urllib
from bs4 import BeautifulSoup

# ポケモン徹底攻略のページに対してスクレイピングかける際のメソッドを集めたクラス
class ScrapeYakkun:

    # main
    def scrape(url, pokemonBean):
        
        soup = util.SoupUtil.getSoupFromURL(url)

        pokemonBean.yakkunId = ScrapeYakkun.scrapeYakkunId(soup)
        pokemonBean.dexNumber = ScrapeYakkun.scrapeDexNumber(soup)
        pokemonBean.name = ScrapeYakkun.scrapeName(soup)
        pokemonBean.englishName = ScrapeYakkun.scrapeEnglishName(soup)
        pokemonBean.status = ScrapeYakkun.scrapeStatus(soup)
        pokemonBean.baseStats = ScrapeYakkun.scrapeBaseStats(soup)
        pokemonBean.type = ScrapeYakkun.scrapeType(soup)
        pokemonBean.eggGroup = ScrapeYakkun.scrapeEggGroup(soup)
        pokemonBean.height = ScrapeYakkun.scrapeHeight(soup)
        pokemonBean.weight = ScrapeYakkun.scrapeWeight(soup)
        pokemonBean.ability = ScrapeYakkun.scrapeAbility(soup)
        pokemonBean.effortValue = ScrapeYakkun.scrapeEffortValue(soup)
        pokemonBean.imagePathSmall = ScrapeYakkun.getImagePathSmall(soup)
        pokemonBean.captureRate = ScrapeYakkun.scrapeCaptureRate(soup)
        pokemonBean.baseEggSteps = ScrapeYakkun.scrapeBaseEggSteps(soup)
        pokemonBean.baseHappiness = ScrapeYakkun.scrapeBaseHappiness(soup)
        pokemonBean.malePercentage = ScrapeYakkun.scrapeMalePercentage(soup)
        pokemonBean.growthRate = ScrapeYakkun.scrapeGrowthRate(soup)
        pokemonBean.captureLocation = ScrapeYakkun.scrapeCaptureLocation(soup)
        pokemonBean.evolution = ScrapeYakkun.scrapeEvolution(soup)
        pokemonBean.move = ScrapeYakkun.scrapeMove(soup)
        
        # get icon image
        id_ = '{0:04d}'.format(pokemonBean.dexNumber) + '{0:02d}'.format(pokemonBean.status[1])
        ScrapeYakkun.scrapeSmallImage(id_, pokemonBean.yakkunId)
        
        nextUrl = None
        if url != entities.WebPage.TETTEIKOURYAKU_BLACEPHALON:
            nextUrl = ScrapeYakkun.getNextURL(soup)
            
        return pokemonBean, nextUrl
        
    # yakkunId #n1
    def scrapeYakkunId(soup):
        answer = None
        url = soup.find("meta", {"property":"og:url"}).get("content")
        list_ = url.split("/")
        answer = list_[len(list_) - 1]
        return answer
    
    # dexNumber # 1
    def scrapeDexNumber(soup):
        centerTagtrs = soup.find_all("tr", {"class":"center"})
        for tag in centerTagtrs:
            if len(tag.find_all("td", text=re.compile("ぜんこくNo."))) != 0:
                dexNumber = tag.find_all("td")[1].get_text()
        return int(dexNumber)

    # name # "フシギダネ"
    def scrapeName(soup):
        layoutLeft = soup.find("div", {"class":"table layout_left"})
        name = layoutLeft.find("th").get_text()
        return name
    
    # englishName # "Bulbasaur"
    def scrapeEnglishName(soup):
        centerTagtrs = soup.find_all("tr", {"class":"center"})
        for tag in centerTagtrs:
            if len(tag.find_all("td", text=re.compile("英語名"))) != 0:
                englishName = tag.find_all("td")[1].get_text()
        return englishName
    
    # status # [フシギダネ, 0](["メガゲンガー", 90], ["アタックフォルム", 1], ...)
    def scrapeStatus(soup):
        answer = None
        statusPart = soup.find_all("ul", {"class":"select_list"})
        if len(statusPart) > 1:
            count = 0
            for part in statusPart[1].find_all("li"):
                if count == 1:
                    normalName = part.get_text()
                if part.find("strong") != None:
                    answer = part.get_text()
                    if count == 0:
                        return [answer, 0]
                    elif answer == "メガ" + normalName:
                        return [answer, 90]
                    elif answer == "メガ" + normalName + "X":
                        return [answer, 91]
                    elif answer == "メガ" + normalName + "Y":
                        return [answer, 92]
                    elif answer.find("のすがた") > -1:
                        return [answer, 49 + count]
                    else:
                        return [answer, count - 1]
                count = count + 1
        return [answer, 0]
        
    # baseStats # [45, 49, 49, 65, 65, 45]
    def scrapeBaseStats(soup):
        return [ScrapeYakkun.scrapeBaseStatsSub(soup, "HP"), ScrapeYakkun.scrapeBaseStatsSub(soup, "こうげき"), ScrapeYakkun.scrapeBaseStatsSub(soup, "ぼうぎょ"), ScrapeYakkun.scrapeBaseStatsSub(soup, "とくこう"), ScrapeYakkun.scrapeBaseStatsSub(soup, "とくぼう"), ScrapeYakkun.scrapeBaseStatsSub(soup, "すばやさ")]
    def scrapeBaseStatsSub(soup, stat):
        answer = None
        baseStatTrs= soup.find("table", {"summary":"詳細データ"}).find_all("tr")
        for tr in baseStatTrs:
            if len(tr.find_all("td", text=re.compile(stat))) != 0:
                answer = int(tr.find_all("td")[1].get_text().split("(")[0])
                break
        return answer
        
    # type # ["くさ", "どく"]
    def scrapeType(soup):
        answer = [None, None]
        typeParts = soup.find("ul", {"class":"type"}).find_all("img")
        count = 0
        for part in typeParts:
            answer[count] = part.get("alt")
            count += 1
        return answer
        
    # eggGroup # ["怪獣", "植物"]
    def scrapeEggGroup(soup):
        answer = [None, None]
        trs = soup.find_all("tr")
        for tr in trs:
            if len(tr.find_all("td", text=re.compile("タマゴグループ"))) != 0:
                groups = tr.find_all("a")
                count = 0
                for group in groups:
                    answer[count] = group.get_text()
                    count =+ 1
        return answer
        
    # height # 0.7
    def scrapeHeight(soup):
        centerTagtrs = soup.find_all("tr", {"class":"center"})
        for tag in centerTagtrs:
            if len(tag.find_all("td", text=re.compile("高さ"))) != 0:
                height = tag.find_all("td")[1].get_text()
                height = float(height.replace("m", ""))
        return height
            
    # weight # 6.9
    def scrapeWeight(soup):
        centerTagtrs = soup.find_all("tr", {"class":"center"})
        for tag in centerTagtrs:
            if len(tag.find_all("td", text=re.compile("重さ"))) != 0:
                if tag.find_all("td")[1].find("li") != None:
                    weight = tag.find_all("td")[1].find_all("ul")[0].find("li").get_text()
                    weight = float(weight.replace("kg", ""))
        return weight
    
    # ability # [["しんりょく", "HPが1/3以下の時、『くさ』タイプの技の威力が1.5倍になる。"], [None, None], ["ようりょくそ", "天気が『ひざしがつよい』の時、『すばやさ』が2倍になる。"]]
    def scrapeAbility(soup):
        answer = [[None, None], [None, None], [None, None]]
        trs = soup.find_all("tr")
        count = 0
        for tr in trs:
            if len(tr.find_all("a", href=re.compile("tokusei"))) != 0:
                if tr.get_text().find("*") > -1:
                    answer[2][0] = tr.find("a").get_text().replace("*","")
                    answer[2][1] = tr.find("td", {"class":"left"}).get_text()
                else:
                    answer[count][0] = tr.find("a").get_text()
                    answer[count][1] = tr.find("td", {"class":"left"}).get_text()
                    count =+ 1
        return answer
        
    # effortValue # [0, 0, 0, 1, 0, 0]
    def scrapeEffortValue(soup):
        return [ScrapeYakkun.scrapeEffortValueSub(soup, "HP"), ScrapeYakkun.scrapeEffortValueSub(soup, "こうげき"), ScrapeYakkun.scrapeEffortValueSub(soup, "ぼうぎょ"), ScrapeYakkun.scrapeEffortValueSub(soup, "とくこう"), ScrapeYakkun.scrapeEffortValueSub(soup, "とくぼう"), ScrapeYakkun.scrapeEffortValueSub(soup, "すばやさ")]
    def scrapeEffortValueSub(soup, stat):
        answer = None
        trs = soup.find_all("tr")
        for tr in trs:
            if len(tr.find_all("img", src=re.compile("img.yakkun.com/bar.gif"))):
                if len(tr.find_all("td", text=re.compile(stat))) != 0:
                    answer = int(tr.find_all("td")[1].get_text().split("(")[0])  
        return answer
    
    # imagePathSmall # ¥C¥....
    def getImagePathSmall(soup):
        return None
        
    # captureRate # 45
    def scrapeCaptureRate(soup):
        trs = soup.find_all("tr")
        answer = None
        for tr in trs:
            if len(tr.find_all("td", text=re.compile("ゲットしやすさ"))) != 0:
                if tr.find_all("td")[1].get_text().find("USUM") > -1:
                    answer = int(tr.find_all("td")[1].get_text().split("/")[0].replace("USUM", "").replace(" ", ""))
                else:
                    answer = int(tr.find_all("td")[1].get_text())
        return answer
    
    # baseEggSteps # 5120
    def scrapeBaseEggSteps(soup):
        trs = soup.find_all("tr")
        answer = None
        for tr in trs:
            if len(tr.find_all("td", text=re.compile("タマゴ歩数"))) != 0:
                cycle = int(tr.find("span").get_text().replace("(サイクル:", "").replace(")", ""))
        answer = int(cycle / 5 * 1280)
        return answer
    
    # baseHappiness # 70
    def scrapeBaseHappiness(soup):
        trs = soup.find_all("tr")
        answer = None
        for tr in trs:
            if len(tr.find_all("td", text=re.compile("初期なつき度"))) != 0:
                answer = int(tr.find_all("td")[1].get_text().replace(" ", ""))
        return answer
    
    # malePercentage # 87.5
    def scrapeMalePercentage(soup):
        trs = soup.find_all("tr")
        answer = None
        for tr in trs:
            if len(tr.find_all("td", text=re.compile("性別"))) != 0:
                if tr.find_all("td")[1].get_text() == "ふめい":
                    return None
                elif tr.find_all("td")[1].get_text().find("♀のみ") > -1:
                    return float(0)
                elif tr.find_all("td")[1].get_text().find("♂のみ") > -1:
                    return float(100)
                else:
                    answer = float(tr.find_all("td")[1].get_text().replace("%", "").replace("♂:", "").split("\xa0/\xa0♀:")[0])
                    break
        return answer
    
    # growthRate # "1050k"
    def scrapeGrowthRate(soup):
        trs = soup.find_all("tr")
        answer = None
        for tr in trs:
            if len(tr.find_all("td", text=re.compile("経験値タイプ"))) != 0:
                growthRate = tr.find_all("td")[1].get_text()
        if growthRate == "60万":
            answer = "600k"
        elif growthRate == "80万":
            answer = "800k"
        elif growthRate == "100万":
            answer = "1000k"
        elif growthRate == "105万":
            answer = "1050k"
        elif growthRate == "125万":
            answer = "1250k"
        elif growthRate == "164万":
            answer = "1640k"
        return answer
    
    # captureLocation # [[None, None, None, None, None, None, None, None]] ([["1番道路", "C", None, None, None, None, None, None], ["テンカラットヒル", None, "最奥空洞", None, None, None, None, None]])
    def scrapeCaptureLocation(soup):
        encounterParts = soup.find("ul", {"class":"encounter"}).find_all("li")
        answer = []
        for areaPart in encounterParts:
            if areaPart.get_text() != "なし":
                area = [None, None, None, None, None, None, None, None]
                if areaPart.find("a") != None:
                    area[0] = areaPart.find("a").get_text()
                else:
                    break
                areaSubs = areaPart.find_all("span")
                for sub in areaSubs:
                    areaSub = sub.get_text()
                    count = 5
                    if areaSub.find("(A)") > -1 or areaSub.find("(B)") > -1 or areaSub.find("(C)") > -1:
                        area[1] = areaSub
                    elif areaSub.find("呼出") > -1:
                        area[2] = areaSub
                    elif areaSub.find("昼") > -1 or areaSub.find("夜") > -1:
                        area[3] = areaSub
                    elif areaSub.find("サン") > -1:
                        area[4] = "us"
                    elif areaSub.find("ムーン") > -1:
                        area[4] = "um"
                    else:
                        area[count] = areaSub
                        count += 1
                answer.append(area)
        return answer
    
    # evolution # None (["n1", "Lv.16"])
    def scrapeEvolution(soup):
        answer = [None, None]
        url = soup.find("meta", {"property":"og:url"}).get("content")
        if soup.find("ul", {"class":"evo_list"}) != None:
            lis = soup.find("ul", {"class":"evo_list"}).find_all("li")
        else:
            return
        selfNum = 0
        count = 0
        for li in lis:
            if li.find("a") != None:
                if url.find(li.find("a").get("href").replace(".", "")) > -1:
                    selfNum = count
                    if li.get_text().find("⇒") > -1:
                        description = li.get_text().split("⇒")[1].replace(" ", "").split("『")[0].replace("\xa0", "")
                        answer[1] = description
            count += 1
        judge = False
        for i in reversed(range(selfNum + 1)):
            if lis[i].find("hr") != None:
                return
            elif lis[i].get("class") != None:
                if lis[i].get("class")[0] == "evo_arrow":
                    judge = True
            elif judge == True and lis[i].find("a") != None:
                answer[0] = lis[i].find("a").get("href").split("/")[-1]
                return answer
    
    # move # [["たいあたり", ”ノーマル”, ”物理”, 40, 100, 35, True, "通常攻撃。(第6世代は威力:50)", "基本"],["なきごえ", ... ]]
    def toInt(script):
        if script == "-":
            return None
        else:
            return int(script)
    def scrapeMove(soup):
        moveRow1s = soup.find_all("tr", {"class" : "move_main_row"})
        moveRow2s = soup.find_all("tr", {"class" : "move_detail_row"})
        answer = []
        for i in range(len(moveRow1s)):
            moveName = moveRow1s[i].find("a").get_text()
            moveAcquiringState = moveRow1s[i].find("td", {"class" : "move_condition_cell"}).get_text()
            moveRowTds = moveRow2s[i].find_all("td")
            moveType = moveRowTds[0].get_text()
            moveDamageCategory = moveRowTds[1].get_text()
            movePower = ScrapeYakkun.toInt(moveRowTds[2].get_text())
            moveAccuracy = ScrapeYakkun.toInt(moveRowTds[3].get_text())
            movePP = ScrapeYakkun.toInt(moveRowTds[4].get_text())
            if moveRowTds[5].get_text() == "×":
                moveContact = False
            elif moveRowTds[5].get_text() == "○":
                moveContact = True
            moveDescription = moveRowTds[6].get_text()
            answer.append([moveName, moveType, moveDamageCategory, movePower, moveAccuracy, movePP, moveContact, moveDescription, moveAcquiringState])
        return answer
    
    # 次のURLをgetするメソッド
    def getNextURL(soup):
        statusPart = soup.find_all("ul", {"class":"select_list"})
        if len(statusPart) > 1:
            index = None
            for part in statusPart[1].find_all("li"):
                if part.find("strong") != None:
                    index = statusPart[1].find_all("li").index(part)
            if index != len(statusPart[1].find_all("li")) - 1:
                url = statusPart[1].find_all("li")[index + 1].a.get("href").replace("/sm/zukan/", "")
                url = entities.WebPage.TETTEIKOURYAKU + url
                return url
            else:
                allATag = soup.find_all("a")
                for aTag in allATag:
                    if aTag.get_text().find(">>") > -1:
                        url = aTag.get("href").replace("./", "")
                        url = entities.WebPage.TETTEIKOURYAKU + url
                        return url
        else:
            allATag = soup.find_all("a")
            for aTag in allATag:
                if aTag.get_text().find(">>") > -1:
                    url = aTag.get("href").replace("./", "")
                    url = entities.WebPage.TETTEIKOURYAKU + url
                    return url
        
    def scrapeSmallImage(id_, yakkunId):
        url = entities.WebPage.TETTEIKOURYAKU_ICON + yakkunId + ".gif"
        try:
            data = urllib.request.urlopen(url).read()
            fname = id_ + ".gif"
            dst_path = entities.WebPage.TETTEIKOURYAKU_ICON_DIRECTORY + fname
            with open(dst_path, mode="wb") as f:
                f.write(data)
            return
        except urllib.error.URLError as e:
            print(e)
            return
    
            
# 技一覧を取得するためのクラス
class ScrapeMoves:
    
    # 変化技、物理技、特殊技それぞれのURLを取得するクラス
    def getURL(url, soup, moveType):
        answer = url.replace(url.split("/")[-1], "") + soup.find("a", text=re.compile(moveType)).get("href").replace("./", "")
        return answer
    
    # getting a list of trs as html
    def getTrList(soup):
        answer = []
        trs = soup.find_all("tr")
        for i in range(len(trs)):
            ans = [None, None]
            if trs[i].find("th") == None:
                if i % 2 == 0:
                    ans[0] = trs[i]
                    ans[1] = trs[i+1]
                    answer.append(ans)
        return answer
    
    # getting moveBean from tr
    def getMoveData(tr, moveBean):
        # 1行目
        tdListBase = tr[0].find_all("td")
        moveBean.name = tdListBase[0].get_text()
        moveBean.type = tdListBase[1].get_text()
        moveBean.damageCategory = tdListBase[2].get_text()
        if tdListBase[3].get_text() != "-":
            moveBean.power = int(tdListBase[3].get_text())
        if tdListBase[4].get_text() != "-":
            moveBean.powerZ = int(tdListBase[4].get_text())
        if tdListBase[5].get_text() != "-":
            moveBean.accuracy = int(tdListBase[5].get_text())
        if tdListBase[6].get_text() != "-":
            moveBean.pp = int(tdListBase[6].get_text())
        if tdListBase[7].get_text().find("直○") > -1:
            moveBean.contact = True
        elif tdListBase[7].get_text().find("直×") > -1:
            moveBean.contact = False
        # 2行目
        tdListDes = tr[1].find_all("td")
        moveBean.target = tdListDes[0].get_text()
        descriptionList = tdListDes[1].get_text().split("Z技:")
        moveBean.description = descriptionList[0]
        if len(descriptionList) > 1:
            moveBean.descriptionZ = descriptionList[1]
        else:
            moveBean.descriptionZ = None

        return moveBean

# 道具一覧を取得するためのクラス
class ScrapeItems:
    
    # 通常の道具、Zクリスタル、メガストーン、きのみ、それぞれのURLを取得するクラス
    def getURL(url, soup, itemType):
        answer = url.replace(url.split("/")[-1], "") + soup.find("a", text=re.compile(itemType)).get("href").replace("./", "")
        return answer
    
    # getting a list of item info
    def getItemInfo(soup):
        answer = []
        trs = soup.find_all("tr")
        j = 0
        for i in range(len(trs)):
            ans = [None, None, None]
            if trs[i].find("th") == None:
                j = j + 1
                if j % 2 == 1:
                    ans[0] = trs[i].find("td", {"class":"c1"}).get_text()
                    ans[1] = trs[i].find_all("td")[-1].get_text()
                    ans[2] = trs[i + 1].find("td").get_text()
                    answer.append(ans)
        return answer
    
    # getti