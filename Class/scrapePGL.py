# -*- coding: utf-8 -*-
from . import bean
from . import util
from . import entities
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScrapePGL():
    
    def initialOperation(driver):
        # PGL起動
        driver.get(entities.WebPage.PGL)
        time.sleep(1)
        # go to フシギダネ
        util.SeleniumUtil.clickElementByLinkText(driver, u"日本語", 5)
        driver.get(entities.WebPage.PGL_RATING_BATTLE)
        time.sleep(1)
        util.SeleniumUtil.clickElementByLinkText(driver, u"ポケモンを選ぶ", 5)
        util.SeleniumUtil.clickElementByLinkText(driver, u"ずかん番号順", 5)
        util.SeleniumUtil.clickElementByXpath(driver, "(//img[contains(@src,'https://n-3ds-pgl-contents.pokemon-gl.com/share/images/spacer.png')])[51]", 5)
        
    def checkIfDataExists(driver):
        check = True
        try:
            checkElement = util.SeleniumUtil.clickElementByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]', 1)
            if checkElement.text == "表示できるデータがありません":
                check = False
        except:
            print("error occured at Class.scrapePGL.checkIfDataExists: No element")
        return
    
    def scrapePglData(driver):
        pglBean = bean.PglBean()
        pglBean.updatedTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        pglBean.name = ScrapePGL.scrapePglName(driver)
        pglBean.pglId = ScrapePGL.scrapePglId(driver)
        pglBean.type = ScrapePGL.scrapePglType(driver)
        pglBean.move = ScrapePGL.scrapePglMove(driver)
        pglBean.pokemonWith = ScrapePGL.scrapePglPokemonWith(driver)
        # click to Ability Tab
        util.SeleniumUtil.clickElementByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[2]/h5/span', 5)
        pglBean.ability = ScrapePGL.scrapePglAbility(driver)
        # click to Nature Tab
        util.SeleniumUtil.clickElementByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[3]/h5/span', 5)
        pglBean.nature = ScrapePGL.scrapePglNature(driver)
        # click to Item Tab
        util.SeleniumUtil.clickElementByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[4]/h5/span', 5)
        pglBean.item = ScrapePGL.scrapePglItem(driver)
        # click to Pokemon Victorious Tab
        util.SeleniumUtil.clickElementByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[4]/h5/span', 5)
        pglBean.pokemonVictorious = None
        pglBean.moveVictorious = None
        pglBean.pokemonDefeated = None
        pglBean.moveDefeated = None
        return pglBean

    def scrapePglName(driver):
        element = util.(driver, '//*[@id="pokemon-detail-common"]/div[3]', 5)
        return element.text
    
    def scrapePglId(driver):
        element = util.SeleniumUtil.getElementByXpath(driver, "(//img[contains(@src,'https://n-3ds-pgl-contents.pokemon-gl.com/share/images/spacer.png')])[51]", 5)
        style = element.get_attribute("style")
        pglId = style.split("pokemon/300/")[-1].split(".png")[0]
        return pglId
    
    def scrapePglType(driver):
        elements = util.SeleniumUtil.getElementsByXpath(driver, '//*[@id="pokemon-detail-common"]/ul/li', 5)
        if len(elements) == 1:
            return [elements[0].text, None]
        elif len(elements) == 2:
            return [elements[0].text, elements[1].text]
        else:
            print("[ scrapePGL.py ] : error occured at line 65. more than 2 elements.")
            return
    
    def scrapePglPokemonWith(driver):
        answer = []
        elements = util.SeleniumUtil.getElementsByXpath(driver, '//*[@id="pokemon-detail-party"]/div[2]/ol/li/div/img', 5)
        for i in range(len(elements)):
            style = elements[i].get_attribute("style")
            pglId = style.split("pokemon/44/")[-1].split(".png")[0]
            pokemonWith = [i + 1, pglId]
            answer.append(pokemonWith)
        return answer
    
    def scrapePglMove(driver):
        elements = util.SeleniumUtil.getElementsByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[1]/div/table/tbody/tr/td', 5)
        answer = []
        for i in range(len(elements)):
            if i % 3 == 0:
                moveList = [None, None, None]
                moveList[0] = elements[i].text
            elif i % 3 == 1:
                moveList[1] = elements[i].text
            elif i % 3 == 2:
                moveList[2] = elements[i].text
                answer.append(moveList)
        return answer

    def scrapePglAbility(driver):
        elements = util.SeleniumUtil.getElementsByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[2]/div/table/tbody/tr/td', 5)
        answer = []
        for i in range(len(elements)):
            if i % 3 == 0:
                moveList = [None, None, None]
                moveList[0] = elements[i].text
            elif i % 3 == 1:
                moveList[1] = elements[i].text
            elif i % 3 == 2:
                moveList[2] = elements[i].text
                answer.append(moveList)
        return answer
    
    def scrapePglNature(driver):
        elements = util.SeleniumUtil.getElementsByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[3]/div/table/tbody/tr/td', 5)
        answer = []
        for i in range(len(elements)):
            if i % 3 == 0:
                moveList = [None, None, None]
                moveList[0] = elements[i].text
            elif i % 3 == 1:
                moveList[1] = elements[i].text
            elif i % 3 == 2:
                moveList[2] = elements[i].text
                answer.append(moveList)
        return answer
    
    def scrapePglItem(driver):
        elements = util.SeleniumUtil.getElementsByXpath(driver, '//*[@id="pokemon-detail-party"]/div[1]/div[4]/div/table/tbody/tr/td', 5)
        answer = []
        for i in range(len(elements)):
            if i % 3 == 0:
                moveList = [None, None, None]
                moveList[0] = elements[i].text
            elif i % 3 == 1:
                moveList[1] = elements[i].text
            elif i % 3 == 2:
                moveList[2] = elements[i].text
                answer.append(moveList)
        return answer