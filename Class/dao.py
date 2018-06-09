# -*- coding: utf-8 -*-

from . import util
from . import bean
from . import entities
from . import scrapeYakkun
import os
import mysql.connector

class Connector(object):
    
    def __init__(self, account):
        self.account = account
    
    def __enter__(self):
        os.system("mysql.server start")
        self.connect = mysql.connector.connect(
            db      = self.account["db"],
            host    = self.account["host"],
            user    = self.account["user"],
            passwd  = self.account["passwd"],
            charset = "utf8")
        return self.connect

    def __exit__(self, exception_type, exception_value, traceback):
        self.connect.close()
        os.system("mysql.server stop")

class Cursor(object):
    
    def __init__(self, connection):
        self.connection = connection
    
    def __enter__(self):
        return self.connection.cursor(buffered=True)
    
    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type:
            self.connection.rollback()
        else:
            self.connection.commit()

class MoveDao:
    
    def insertMoveData(moveBean, connect):
        # check
        with Cursor(connect) as cursor:
            if MoveDao.checkIfExists(moveBean.name, cursor):
                return None
        # type_id
        typeID = util.DaoUtil.insertDataAndGetID(moveBean.type, None, connect, "type")
        # insert
        script = "INSERT INTO move (name, type_id, damage_category, power, power_z, accuracy, pp, contact, target, description, description_z) VALUES (" + util.DaoUtil.scriptMakeToString(moveBean.name) + ", " + util.DaoUtil.scriptMakeToString(typeID) + ", " + util.DaoUtil.scriptMakeToString(moveBean.damageCategory) + ", " + util.DaoUtil.scriptMakeToString(moveBean.power) + ", " + util.DaoUtil.scriptMakeToString(moveBean.powerZ) + ", " + util.DaoUtil.scriptMakeToString(moveBean.accuracy) + ", " + util.DaoUtil.scriptMakeToString(moveBean.pp) + ", " + util.DaoUtil.scriptMakeToString(moveBean.contact) + ", " + util.DaoUtil.scriptMakeToString(moveBean.target) + ", " + util.DaoUtil.scriptMakeToString(moveBean.description) + ", " + util.DaoUtil.scriptMakeToString(moveBean.descriptionZ) + ")"
        with Cursor(connect) as cursor:
            cursor.execute(script)

    def checkIfExists(name, cursor):
        script = "SELECT id FROM move WHERE name = " + util.DaoUtil.scriptMakeToString(name)
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True
    
    def listToMoveBean(list_, moveBean):
        moveBean.name = list_[0]
        moveBean.type = list_[1]
        moveBean.damageCategory = list_[2]
        moveBean.power = list_[3] if list_[3] != "-" else None
        moveBean.powerZ = None
        moveBean.accuracy = list_[4] if list_[4] != "-" else None
        moveBean.pp = list_[5]
        moveBean.contact = list_[6]
        moveBean.target = None
        moveBean.description = list_[7]
        moveBean.descriptionZ = None
        return moveBean
        
    
class PokemonDao:
    
    def insertPkmBeanData(pokemonBean, connect):
        shapedBean = PokemonDao.pkmBeanIntoShape(pokemonBean, connect)
        script = "INSERT INTO pokemon (id, yakkun_id, dex_number, name, english_name, status, base_stats_H, base_stats_A, base_stats_B, base_stats_C, base_stats_D, base_stats_S, type1_id, type2_id, egg_group1_id, egg_group2_id, height, weight, ability1_id, ability2_id, hidden_ability_id, effort_value_H, effort_value_A, effort_value_B, effort_value_C, effort_value_D, effort_value_S, capture_rate, base_egg_steps, base_happiness, male_percentage, growth_rate_id) VALUES (" + util.DaoUtil.scriptMakeToString(shapedBean[0]) + ", " + util.DaoUtil.scriptMakeToString(pokemonBean.yakkunId)+ ", " + util.DaoUtil.scriptMakeToString(shapedBean[1] )+ ", " + util.DaoUtil.scriptMakeToString(shapedBean[2]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[3]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[4] )+ ", " + util.DaoUtil.scriptMakeToString(shapedBean[5]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[6]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[7] )+ ", " + util.DaoUtil.scriptMakeToString(shapedBean[8]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[9]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[10]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[11]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[12]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[13]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[14]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[15]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[16]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[17]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[18]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[19]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[20]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[21]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[22]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[23]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[24]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[25]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[26]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[27]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[28]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[29]) + ", " + util.DaoUtil.scriptMakeToString(shapedBean[30]) + ") ON DUPLICATE KEY UPDATE id = " + util.DaoUtil.scriptMakeToString(shapedBean[0]) + ", yakkun_id = " + util.DaoUtil.scriptMakeToString(pokemonBean.yakkunId)+ ", dex_number = " + util.DaoUtil.scriptMakeToString(shapedBean[1]) + ", name = " + util.DaoUtil.scriptMakeToString(shapedBean[2]) + ", english_name = " + util.DaoUtil.scriptMakeToString(shapedBean[3] )+ ", status = " + util.DaoUtil.scriptMakeToString(shapedBean[4]) + ", base_stats_H = " + util.DaoUtil.scriptMakeToString(shapedBean[5]) + ", base_stats_A = " + util.DaoUtil.scriptMakeToString(shapedBean[6] )+ ", base_stats_B = " + util.DaoUtil.scriptMakeToString(shapedBean[7]) + ", base_stats_C = " + util.DaoUtil.scriptMakeToString(shapedBean[8]) + ", base_stats_D = " + util.DaoUtil.scriptMakeToString(shapedBean[9]) + ", base_stats_S = " + util.DaoUtil.scriptMakeToString(shapedBean[10]) + ", type1_id = " + util.DaoUtil.scriptMakeToString(shapedBean[11]) + ", type2_id = " + util.DaoUtil.scriptMakeToString(shapedBean[12]) + ", egg_group1_id = " + util.DaoUtil.scriptMakeToString(shapedBean[13]) + ", egg_group2_id = " + util.DaoUtil.scriptMakeToString(shapedBean[14]) + ", height = " + util.DaoUtil.scriptMakeToString(shapedBean[15]) + ", weight = " + util.DaoUtil.scriptMakeToString(shapedBean[16]) + ", ability1_id = " + util.DaoUtil.scriptMakeToString(shapedBean[17]) + ", ability2_id = " + util.DaoUtil.scriptMakeToString(shapedBean[18]) + ", hidden_ability_id = " + util.DaoUtil.scriptMakeToString(shapedBean[19]) + ", effort_value_H = " + util.DaoUtil.scriptMakeToString(shapedBean[20]) + ", effort_value_A = " + util.DaoUtil.scriptMakeToString(shapedBean[21]) + ", effort_value_B = " + util.DaoUtil.scriptMakeToString(shapedBean[22]) + ", effort_value_C = " + util.DaoUtil.scriptMakeToString(shapedBean[23]) + ", effort_value_D = " + util.DaoUtil.scriptMakeToString(shapedBean[24]) + ", effort_value_S = " + util.DaoUtil.scriptMakeToString(shapedBean[25]) + ", capture_rate = " + util.DaoUtil.scriptMakeToString(shapedBean[26]) + ", base_egg_steps = " + util.DaoUtil.scriptMakeToString(shapedBean[27]) + ", base_happiness = " + util.DaoUtil.scriptMakeToString(shapedBean[28]) + ", male_percentage = " + util.DaoUtil.scriptMakeToString(shapedBean[29]) + ", growth_rate_id = " + util.DaoUtil.scriptMakeToString(shapedBean[30])
        with Cursor(connect) as cursor:
            cursor.execute(script)
    
    def pkmBeanIntoShape(pokemonBean, connect):
        # make ID
        id_ = '{0:04d}'.format(pokemonBean.dexNumber) + '{0:02d}'.format(pokemonBean.status[1])
        dexNumber = pokemonBean.dexNumber
        name = pokemonBean.name
        englishName = pokemonBean.englishName
        status = pokemonBean.status[0] if pokemonBean.status[0] != None else pokemonBean.name
        baseStatsH = pokemonBean.baseStats[0]
        baseStatsA = pokemonBean.baseStats[1]
        baseStatsB = pokemonBean.baseStats[2]
        baseStatsC = pokemonBean.baseStats[3]
        baseStatsD = pokemonBean.baseStats[4]
        baseStatsS = pokemonBean.baseStats[5]
        type1ID =  util.DaoUtil.insertDataAndGetID(pokemonBean.type[0], None, connect, "type")
        type2ID =  util.DaoUtil.insertDataAndGetID(pokemonBean.type[1], None, connect, "type")
        eggGroup1ID = util.DaoUtil.insertDataAndGetID(pokemonBean.eggGroup[0], None, connect, "egg_group")
        eggGroup2ID = util.DaoUtil.insertDataAndGetID(pokemonBean.eggGroup[1], None, connect, "egg_group")
        height = pokemonBean.height
        weight = pokemonBean.weight
        ability1ID = util.DaoUtil.insertDataAndGetID(pokemonBean.ability[0][0], pokemonBean.ability[0][1], connect, "ability")
        ability2ID = util.DaoUtil.insertDataAndGetID(pokemonBean.ability[1][0], pokemonBean.ability[1][1], connect, "ability")
        hiddenAbilityID = util.DaoUtil.insertDataAndGetID(pokemonBean.ability[2][0], pokemonBean.ability[2][1], connect, "ability")
        effortValueH = pokemonBean.effortValue[0]
        effortValueA = pokemonBean.effortValue[1]
        effortValueB = pokemonBean.effortValue[2]
        effortValueC = pokemonBean.effortValue[3]
        effortValueD = pokemonBean.effortValue[4]
        effortValueS = pokemonBean.effortValue[5]
        captureRate = pokemonBean.captureRate
        baseEggSteps = pokemonBean.baseEggSteps
        baseHappiness = pokemonBean.baseHappiness
        malePercentage = pokemonBean.malePercentage
        growthRateID = util.DaoUtil.insertDataAndGetID(pokemonBean.growthRate, None, connect, "growth_rate")
        return [id_, dexNumber, name, englishName, status, baseStatsH, baseStatsA, baseStatsB, baseStatsC, baseStatsD, baseStatsS, type1ID, type2ID, eggGroup1ID, eggGroup2ID, height, weight, ability1ID, ability2ID, hiddenAbilityID, effortValueH, effortValueH, effortValueB, effortValueC, effortValueD, effortValueS, captureRate, baseEggSteps, baseHappiness, malePercentage, growthRateID]
        
    def checkIfExists(id_, cursor):
        script = "SELECT name FROM pokemon WHERE id = " + util.DaoUtil.scriptMakeToString(id_)
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True
        
    def checkIfExistsByYakkunId(id_, cursor):
        script = "SELECT name FROM pokemon WHERE yakkun_id = " + util.DaoUtil.scriptMakeToString(id_)
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True
    
    def yakkunIdToId(yakkunId, cursor):
        script = "SELECT id FROM pokemon WHERE yakkun_id = " + util.DaoUtil.scriptMakeToString(yakkunId)
        cursor.execute(script)
        return cursor.fetchone()[0]
    
class AcquirableMoveDao:
    
    def insertAcquirableMovesData(pokemonBean, connect):
        pkmID = '{0:04d}'.format(pokemonBean.dexNumber) + '{0:02d}'.format(pokemonBean.status[1])
        moveList = pokemonBean.move
        for i in range(len(moveList)):
            # get move_id
            with Cursor(connect) as cursor:
                moveID = util.DaoUtil.getID(moveList[i][0], cursor, "move")
            if moveID == False:
                mvBean = bean.MoveBean()
                mvBean = MoveDao.listToMoveBean(moveList[i], mvBean)
                MoveDao.insertMoveData(mvBean, connect)
                print("[dao.py] : move " + moveList[i][0] + " was not in move database, insert done")
                # get move_id
                with Cursor(connect) as cursor:
                    moveID = util.DaoUtil.getID(moveList[i][0], cursor, "move")
            if moveList[i][8].find("Lv.") > -1:
                level = int(moveList[i][8].replace("Lv.", ""))
                acquiringState = "Lv."
                acquiringStateId = util.DaoUtil.insertDataAndGetID(acquiringState, None, connect, "acquiring_state")
            else:
                level = None
                acquiringStateId = util.DaoUtil.insertDataAndGetID(moveList[i][8], None, connect, "acquiring_state")
            # check
            with Cursor(connect) as cursor:
                if AcquirableMoveDao.checkIfExists(moveID, pkmID, acquiringStateId, level, cursor):
                    return None
            # insert
            script = "INSERT INTO acquirable_moves (move_id, pokemon_id, acquiring_state_id, level) VALUES (" + util.DaoUtil.scriptMakeToString(moveID) + ", " + util.DaoUtil.scriptMakeToString(pkmID) + ", " + util.DaoUtil.scriptMakeToString(acquiringStateId) + ", " + util.DaoUtil.scriptMakeToString(level) + ")"
            with Cursor(connect) as cursor:
                cursor.execute(script)
        
    def checkIfExists(moveID, pokemonID, acquiringStateId, level, cursor):
        script = "SELECT id FROM acquirable_moves WHERE move_id = " + util.DaoUtil.scriptMakeToString(moveID) + " and pokemon_id = " + util.DaoUtil.scriptMakeToString(pokemonID) + " and acquiring_state_id = " + util.DaoUtil.scriptMakeToString(acquiringStateId) + " and level = " + util.DaoUtil.scriptMakeToString(level)
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True

class EvolutionDao:
    
    # put yakkunId to database for now, b/c for ex), pichu not in database for pikachu
    def insertEvolutionData(pokemonBean, connect):
        pkmId = '{0:04d}'.format(pokemonBean.dexNumber) + '{0:02d}'.format(pokemonBean.status[1])
        evolutionList = pokemonBean.evolution
        if evolutionList == None:
            return
        pkmIdYakkunPre = evolutionList[0]
        # check if pkmIdYakkunPre has an id in database, if not, go and get it
        with Cursor(connect) as cursor:
            if PokemonDao.checkIfExistsByYakkunId(pkmIdYakkunPre, cursor):
                pkmIdPre = PokemonDao.yakkunIdToId(pkmIdYakkunPre, cursor)
            else:
                pkmIdPre = EvolutionDao.insertAndGetIdBeforehead(pkmIdYakkunPre, cursor)
        # check
        with Cursor(connect) as cursor:
            if EvolutionDao.checkIfExists(pkmIdPre, pkmId, cursor):
                return
        # process_id
        processId = util.DaoUtil.insertDataAndGetID(evolutionList[1], None, connect, "evolution_process")
        # insert
        script = "INSERT INTO evolution (pokemon1_id, pokemon2_id, process_id) VALUES (" + util.DaoUtil.scriptMakeToString(pkmIdPre) + ", " + util.DaoUtil.scriptMakeToString(pkmId) + ", " + util.DaoUtil.scriptMakeToString(processId) + ")"
        with Cursor(connect) as cursor:
            cursor.execute(script)
    
    def checkIfExists(pokemonIdPre, pokemonId, cursor):
        script = "SELECT process_id FROM evolution WHERE pokemon1_id = " + util.DaoUtil.scriptMakeToString(pokemonIdPre) + " and pokemon2_id = " + util.DaoUtil.scriptMakeToString(pokemonId)
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True
    
    def insertAndGetIdBeforehead(yakkunId, cursor):
        url = entities.WebPage.TETTEIKOURYAKU + yakkunId
        soup = util.SoupUtil.getSoupFromURL(url)
        dexNumber = scrapeYakkun.ScrapeYakkun.scrapeDexNumber(soup)
        status = scrapeYakkun.ScrapeYakkun.scrapeStatus(soup)
        id_ = '{0:04d}'.format(dexNumber) + '{0:02d}'.format(status[1])
        script = "INSERT INTO pokemon (id, yakkun_id, dex_number) VALUES (" + util.DaoUtil.scriptMakeToString(id_) + ", " + util.DaoUtil.scriptMakeToString(yakkunId) + ", " + util.DaoUtil.scriptMakeToString(dexNumber) + ")"
        cursor.execute(script)
        return id_
    
class CaptureLocationDao:
    
    def insertCaptureLocationData(pokemonBean, connect):
        pkmID = '{0:04d}'.format(pokemonBean.dexNumber) + '{0:02d}'.format(pokemonBean.status[1])
        captureLocationList = pokemonBean.captureLocation
        if captureLocationList == None:
            return
        # check
        with Cursor(connect) as cursor:
            for captureLocation_ in captureLocationList:
                if CaptureLocationDao.checkIfExists(pkmID, captureLocation_, cursor):
                    print("[ dao.py ] : One of the capture locations already exists for " + pokemonBean.name)
                    return None
        # insert
        for captureLocation_ in captureLocationList:
            script = "INSERT INTO capture_location (pokemon_id, location, sublocation, help_call, capture_time, cartridge_peculiar, note1, note2, note3) VALUES (" + util.DaoUtil.scriptMakeToString(pkmID) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[0]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[1]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[2]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[3]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[4]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[5]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[6]) + ", " + util.DaoUtil.scriptMakeToString(captureLocation_[7]) + ")"
            with Cursor(connect) as cursor:
                cursor.execute(script)
        
    def checkIfExists(pokemonID, captureLocation, cursor):
        script = "SELECT id FROM capture_location WHERE pokemon_id = " + util.DaoUtil.scriptMakeToString(pokemonID) + " and location = " + util.DaoUtil.scriptMakeToString(captureLocation[0]) + " and sublocation = " + util.DaoUtil.scriptMakeToString(captureLocation[1]) + " and help_call = " + util.DaoUtil.scriptMakeToString(captureLocation[2]) + " and capture_time = " + util.DaoUtil.scriptMakeToString(captureLocation[3]) + " and cartridge_peculiar = " + util.DaoUtil.scriptMakeToString(captureLocation[4]) + " and note1 = " + util.DaoUtil.scriptMakeToString(captureLocation[5]) + " and note2 = " + util.DaoUtil.scriptMakeToString(captureLocation[6]) + " and note3 = " + util.DaoUtil.scriptMakeToString(captureLocation[7])
        cursor.execute(script)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True

class WikiDao:
    
    def getEnglishNameList(connect):
        script = "SELECT DISTINCT english_name from pokemon"
        with Cursor(connect) as cursor:
            cursor.execute(script)
            result = cursor.fetchall()
        return result
            
    def getDexNumberbyEnglishName(engName, connect):
        script = "SELECT dex_number FROM pokemon WHERE english_name = " + util.DaoUtil.scriptMakeToString(engName)
        with Cursor(connect) as cursor:
            cursor.execute(script)
            result = cursor.fetchone()
        return result[0]
    
class ItemDao:
    
    def insertItemData(itemInfo, connect):
        if ItemDao.selectIdByName(itemInfo[0], connect) != False:
            print("[ dao.py ] : Item Data already exists for " + itemInfo[0])
            return
        script = "INSERT INTO item (name, description, acquiring_method) VALUES (" + util.DaoUtil.scriptMakeToString(itemInfo[0]) + ", " + util.DaoUtil.scriptMakeToString(itemInfo[1]) + ", " + util.DaoUtil.scriptMakeToString(itemInfo[2]) + ")"
        with Cursor(connect) as cursor:
            cursor.execute(script)
    
    def selectIdByName(name, connect):
        script = "SELECT id FROM pokemon WHERE name = " + util.DaoUtil.scriptMakeToString(name)
        with Cursor(connect) as cursor:
            cursor.execute(script)
            result = cursor.fetchone()
        if result == None:
            return False
        else:
            return result[0]