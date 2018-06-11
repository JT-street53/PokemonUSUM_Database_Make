# -*- coding: utf-8 -*-
from Class import bean
from Class import entities
from Class import scrapePGL
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(driver, xpath):
    # push the asigned button
    util.SeleniumUtil.clickElementByXpath(driver, xpath, 5)
    # check if data exists
    if scrapePGL.ScrapePGL.checkIfDataExists(driver):
        # get info
        pglBean = scrapePGL.ScrapePGL.scrapePGLData(driver)
        # 紐づけ

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
    
    #main()

    
    '''
    executable_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(executable_path)
    scrapePGL.ScrapePGL.initialOperation(driver)
    '''
    scrapePGL.ScrapePGL.scrapePGLId(driver)
    