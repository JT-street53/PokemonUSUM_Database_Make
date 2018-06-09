# -*- coding: utf-8 -*-
from Class import bean
from Class import entities
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape():
    



def main():
    # chromedriverのpath
    executable_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(executable_path)
    # PGL起動
    driver.get(entities.WebPage.PGL)
    time.sleep(1)
    

if __name__ == '__main__':
    