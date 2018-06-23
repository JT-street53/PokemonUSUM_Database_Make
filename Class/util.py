# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import dao

class SoupUtil:

    def getSoupFromURL(url):
        response = requests.get(url)
        time.sleep(1)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
class DaoUtil:
    
    def scriptMakeToString(obj):
        answer = ""
        if obj == None:
            answer = "NULL"
        elif type(obj) == str:
            if obj.find("'") > -1:
                answer = '"' + obj + '"'
            else:
                answer = "'" + obj + "'"
        elif type(obj) == int:
            answer = str(obj)
        elif type(obj) == float:
            answer = str(obj)
        elif type(obj) == bool:
            if obj:
                answer = "true"
            else:
                answer = "false"
        return answer
    
    def insertDataAndGetID(obj1, obj2, connect, tableName):
        if obj1 == None:
            return None
        with dao.Cursor(connect) as cursor:
            id_ = DaoUtil.getID(obj1, cursor, tableName)
        if id_ == False:
            with dao.Cursor(connect) as cursor:
                DaoUtil.insertData(obj1, obj2, cursor, tableName)
            with dao.Cursor(connect) as cursor:
                id_ = DaoUtil.getID(obj1, cursor, tableName)
        return id_

    def insertData(obj1, obj2, cursor, tableName):
        script = "INSERT INTO " + tableName + " (name) VALUES (" + DaoUtil.scriptMakeToString(obj1) + ")" if obj2 == None else "INSERT INTO " + tableName + " (name, description) VALUES (" + DaoUtil.scriptMakeToString(obj1) + ", " + DaoUtil.scriptMakeToString(obj2) + ")"
        cursor.execute(script)
        
    def getID(obj, cursor, tableName):
        script = "SELECT id FROM " + tableName + " WHERE name = " + DaoUtil.scriptMakeToString(obj)
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return result[0]

class SeleniumUtil:
    
    def clickElementByXpath(driver, xpath, waitingTime):
        wait = WebDriverWait(driver, waitingTime)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            time.sleep(0.1)
            element.click()
            time.sleep(0.1)
        except:
            print("[ util.py ] : error occured at clicking element from xpath")
        return
    
    def clickElementByLinkText(driver, word, waitingTime):
        wait = WebDriverWait(driver, waitingTime)
        try:
            element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, word)))
            time.sleep(0.1)
            element.click()
            time.sleep(0.1)
        except:
            print("[ util.py ] : error occured at clicking element from link text")
            return
    
    def getElementByXpath(driver, xpath, waitingTime):
        wait = WebDriverWait(driver, waitingTime)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            element = None
        return element
    
    def getElementsByXpath(driver, xpath, waitingTime):
        wait = WebDriverWait(driver, waitingTime)
        try:
            element = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except:
            element = None
        return element
        