# -*- coding: utf-8 -*-
from Class import bean
from Class import entities
from Class import scrapePGL
from Class import util
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(driver, xpath):
    # push the asigned button
    util.SeleniumUtil.clickElementByXpath(driver, xpath, 5)
    util.SeleniumUtil.clickElementByXpath(driver, '//*[@id="battle-report-pokemon-detail"]/div[2]/div[2]/div[1]/ul/li[1]/a/span', 5)
    time.sleep(0.1)
    # check if data exists
    if scrapePGL.ScrapePGL.checkIfDataExists(driver, '//*[@id="pokemon-detail-party"]/div[1]'):
        # get info
        pglBean = scrapePGL.ScrapePGL.scrapePglData(driver)
        # 紐づけ
        print("success for " + pglBean.name)
        # put in dao
        print("[ scrapePGL.py ] : Scraping & Installing " + pglBean.name + " from Pokemon Global Link.")
    # go to next pokemon
    scrape(driver, '//*[@id="battle-report-pokemon-detail"]/div[2]/div[2]/p[2]')

def main():
    # chromedriverのpath
    executable_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(executable_path)
    # PGLのフシギダネまで進む
    scrapePGL.ScrapePGL.initialOperation(driver)
    # scrape起動。xpathはフシギダネ画面上でのシングルバトルボタン
    scrape(driver, '//*[@id="battle-report-pokemon-detail"]/div[2]/div[1]/ul/li[2]')

if __name__ == '__main__':
    
    main()
